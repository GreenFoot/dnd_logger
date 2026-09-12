"""Import shim for the Mistral SDK client class.

The ``mistralai`` distribution changed its package layout between major
versions: 1.x ships a regular package exposing ``mistralai.sdk.Mistral``,
while 2.x turned ``mistralai`` into a namespace package and moved the SDK
to ``mistralai.client.Mistral``. Importing the wrong path raises
``ModuleNotFoundError`` at runtime, which is what happened in frozen builds
(built against 2.x) when the source targeted the 1.x path.

Every call site should use :func:`mistral_class` instead of importing
``Mistral`` directly.
"""

import importlib

_CANDIDATES = ("mistralai.client", "mistralai.sdk", "mistralai")

_cached = None


def mistral_class():
    """Return the ``Mistral`` client class from whichever layout is installed.

    Returns:
        type: The ``Mistral`` SDK client class.

    Raises:
        ImportError: If no installed ``mistralai`` layout exposes ``Mistral``.
    """
    global _cached  # pylint: disable=global-statement
    if _cached is not None:
        return _cached
    errors = []
    for module_name in _CANDIDATES:
        try:
            module = importlib.import_module(module_name)
        except ImportError as exc:
            errors.append(f"{module_name}: {exc}")
            continue
        client = getattr(module, "Mistral", None)
        if client is not None:
            _cached = client
            return client
        errors.append(f"{module_name}: no 'Mistral' attribute")
    raise ImportError("Could not import the Mistral client class (" + "; ".join(errors) + ")")
