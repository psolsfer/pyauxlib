"""YAML-related functions."""
import logging
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

logger = logging.getLogger(__name__)


def load_yaml(file: Path) -> Any:
    """Load a yaml file and returns its contents.

    Returns an empty dictionary if the file is not found.

    Parameters
    ----------
    file : Path
        file

    Returns
    -------
    Any
        The contents of the yaml file.
    """
    yaml = YAML(typ="safe")
    try:
        with file.open() as f:
            conf = yaml.load(f)
            if conf is None:
                return {}
    except YAMLError as e:
        logger.warning("Error parsing the file '%s': %s", file, str(e))
        raise

    except FileNotFoundError as e:
        logger.warning("File '%s' was not found: %s", file, str(e))
        raise

    return conf
