import functools
import logging
import os
import pathlib

from nodc_bvol.bvol_nomp import BvolNomp
from nodc_bvol.translate_bvol_name import TranslateBvolName
from nodc_bvol.translate_bvol_name_size import TranslateBvolNameSize


def get_user_given_config_dir() -> pathlib.Path | None:
    path = pathlib.Path(os.getcwd()) / "config_directory.txt"
    if not path.exists():
        return
    with open(path) as fid:
        config_path = fid.readline().strip()
        if not config_path:
            return
        config_path = pathlib.Path(config_path)
        if not config_path.exists():
            return
        return config_path


logger = logging.getLogger(__name__)

CONFIG_ENV = "NODC_CONFIG"

home = pathlib.Path.home()
OTHER_CONFIG_SOURCES = [
    home / "NODC_CONFIG",
    home / ".NODC_CONFIG",
    home / "nodc_config",
    home / ".nodc_config",
]

CONFIG_FILE_NAMES = [
    "bvol_nomp.txt",
    "translate_bvol_name.txt",
    "translate_bvol_name_size.txt",
]


CONFIG_DIRECTORY = None
conf_dir = get_user_given_config_dir()
if conf_dir:
    CONFIG_DIRECTORY = conf_dir
else:
    if os.getenv(CONFIG_ENV) and pathlib.Path(os.getenv(CONFIG_ENV)).exists():
        CONFIG_DIRECTORY = pathlib.Path(os.getenv(CONFIG_ENV))
    else:
        for directory in OTHER_CONFIG_SOURCES:
            if directory.exists():
                CONFIG_DIRECTORY = directory
                break


def get_config_path(name: str = None) -> pathlib.Path:
    if not CONFIG_DIRECTORY:
        raise NotADirectoryError(
            f"Config directory not found. Environment path {CONFIG_ENV} does not seem to be set and not other config directory was found. "
        )
    if name not in CONFIG_FILE_NAMES:
        raise FileNotFoundError(f'No config file with name "{name}" exists')
    path = CONFIG_DIRECTORY / name
    if not path.exists():
        raise FileNotFoundError(f"Could not find config file {name}")
    return path


@functools.cache
def get_translate_bvol_name_object() -> "TranslateBvolName":
    path = get_config_path("translate_bvol_name.txt")
    return TranslateBvolName(path)


@functools.cache
def get_translate_bvol_name_size_object() -> "TranslateBvolNameSize":
    path = get_config_path("translate_bvol_name_size.txt")
    return TranslateBvolNameSize(path)


@functools.cache
def get_bvol_nomp_object() -> "BvolNomp":
    path = get_config_path("bvol_nomp.txt")
    return BvolNomp(path)


if __name__ == "__main__":
    tran_name = get_translate_bvol_name_object()
    tran_size = get_translate_bvol_name_size_object()
    nomp = get_bvol_nomp_object()
    mapper = nomp.get_species_to_aphia_id_mapper()
    # mapper = nomp.get_carbon_per_volume_mapper()

    _mapper = tran_size.get_scientific_name_from_to_mapper()
