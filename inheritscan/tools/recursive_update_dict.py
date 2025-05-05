from inheritscan.tools.logging.logger import get_logger

log = get_logger(__name__)


def recursive_update(d, u):
    """Recursively update dictionary d with values from u."""
    for k, v in u.items():
        if isinstance(v, dict) and isinstance(d.get(k), dict):
            recursive_update(d[k], v)
        else:
            d[k] = v
    return d
