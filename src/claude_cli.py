"""Claude CLI backend — use a locally installed `claude` executable for summarization.

The CLI is optional: when it is not installed the app falls back to the Mistral
chat API. Transcription always goes through Mistral regardless of this backend.
"""

import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile

log = logging.getLogger(__name__)

# Aliases the CLI always accepts, mapped to the latest model of each family.
_ALIASES = ("opus", "sonnet", "haiku", "fable")

# Fallback list used when the entitlement cache cannot be read.
_FALLBACK_MODELS = list(_ALIASES)

_CLI_TIMEOUT = 900  # seconds — summaries of long transcripts can take a while

_cached_path: str | None = None
_path_resolved = False


def _no_window_kwargs() -> dict:
    """Return subprocess kwargs that suppress a console window on Windows."""
    if sys.platform != "win32":
        return {}
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return {
        "startupinfo": startupinfo,
        "creationflags": subprocess.CREATE_NO_WINDOW,
    }


def _candidate_paths() -> list[str]:
    """Return plausible install locations for the Claude CLI."""
    home = os.path.expanduser("~")
    names = ("claude.exe", "claude.cmd", "claude") if sys.platform == "win32" else ("claude",)
    roots = [
        os.path.join(home, ".local", "bin"),
        os.path.join(home, "AppData", "Roaming", "npm"),
        os.path.join(home, ".npm-global", "bin"),
        "/usr/local/bin",
    ]
    return [os.path.join(root, name) for root in roots for name in names]


def find_executable(refresh: bool = False) -> str | None:
    """Locate the Claude CLI executable.

    Args:
        refresh: Re-run the lookup instead of using the cached result.

    Returns:
        Absolute path to the executable, or None when it is not installed.
    """
    global _cached_path, _path_resolved
    if _path_resolved and not refresh:
        return _cached_path

    path = shutil.which("claude")
    if not path:
        for candidate in _candidate_paths():
            if os.path.isfile(candidate):
                path = candidate
                break

    _cached_path = path
    _path_resolved = True
    return path


def is_available(refresh: bool = False) -> bool:
    """Return True when a Claude CLI executable can be found."""
    return find_executable(refresh) is not None


def get_version() -> str:
    """Return the CLI version string, or an empty string when unavailable."""
    exe = find_executable()
    if not exe:
        return ""
    try:
        result = subprocess.run(
            [exe, "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
            check=False,
            **_no_window_kwargs(),
        )
        return (result.stdout or "").strip()
    except (OSError, subprocess.SubprocessError) as e:
        log.warning("Could not read Claude CLI version: %s", e)
        return ""


def _entitled_models() -> list[str]:
    """Read the CLI's cached model entitlements from ~/.claude.json."""
    path = os.path.join(os.path.expanduser("~"), ".claude.json")
    if not os.path.isfile(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        log.warning("Could not read Claude CLI config: %s", e)
        return []
    models = []
    for entry in data.get("modelAccessCache") or []:
        if isinstance(entry, dict) and entry.get("entitled") and entry.get("apiName"):
            models.append(entry["apiName"])
    for entry in data.get("additionalModelOptionsCache") or []:
        if isinstance(entry, dict) and entry.get("value"):
            models.append(entry["value"])
    return models


def list_models() -> list[str]:
    """Return the models usable with the local CLI.

    The family aliases always come first (they track the latest model of each
    family), followed by the concrete models this account is entitled to.

    Returns:
        List of model identifiers, de-duplicated and ordered for display.
    """
    if not is_available():
        return []
    models = list(_ALIASES)
    seen = set(models)
    for name in sorted(_entitled_models()):
        if name not in seen:
            models.append(name)
            seen.add(name)
    return models or list(_FALLBACK_MODELS)


def complete(prompt: str, system_prompt: str = "", model: str = "", timeout: int = _CLI_TIMEOUT) -> str:
    """Run a one-shot prompt through the Claude CLI and return its answer.

    The prompt is passed on stdin so transcript-sized inputs do not hit the
    Windows command-line length limit. Tools and MCP servers are disabled so the
    CLI behaves like a plain chat completion.

    Args:
        prompt: The user message.
        system_prompt: Optional system prompt.
        model: Model identifier or family alias; empty uses the CLI default.
        timeout: Maximum run time in seconds.

    Returns:
        The assistant's text response.

    Raises:
        RuntimeError: If the CLI is missing, times out, or reports an error.
    """
    exe = find_executable()
    if not exe:
        raise RuntimeError("Claude CLI not found")

    cmd = [exe, "--print", "--output-format", "json", "--tools", "", "--strict-mcp-config"]
    if model:
        cmd += ["--model", model]
    if system_prompt:
        cmd += ["--system-prompt", system_prompt]

    try:
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
            cwd=tempfile.gettempdir(),
            **_no_window_kwargs(),
        )
    except subprocess.TimeoutExpired as e:
        raise RuntimeError(f"Claude CLI timed out after {timeout}s") from e
    except OSError as e:
        raise RuntimeError(f"Could not run the Claude CLI: {e}") from e

    stdout = (result.stdout or "").strip()
    if not stdout:
        raise RuntimeError((result.stderr or "").strip() or f"Claude CLI exited with code {result.returncode}")

    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        # Older CLI versions may print plain text despite --output-format json
        return stdout

    if payload.get("is_error"):
        raise RuntimeError(payload.get("result") or payload.get("subtype") or "Claude CLI returned an error")
    text = payload.get("result", "")
    if not text:
        raise RuntimeError("Claude CLI returned an empty response")
    return text
