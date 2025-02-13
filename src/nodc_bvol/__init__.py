import functools
import logging
import os
import pathlib

from nodc_bvol.bvol_nomp import BvolNomp
from nodc_bvol.translate_bvol_name import TranslateBvolName
from nodc_bvol.translate_bvol_name_size import TranslateBvolNameSize

logger = logging.getLogger(__name__)

CONFIG_ENV = 'NODC_CONFIG'

CONFIG_FILE_NAMES = [
    'bvol_nomp.txt',
    'translate_bvol_name.txt',
    'translate_bvol_name_size.txt',
]


CONFIG_DIRECTORY = None
if os.getenv(CONFIG_ENV):
    CONFIG_DIRECTORY = pathlib.Path(os.getenv(CONFIG_ENV))


def get_config_path(name: str) -> pathlib.Path:
    if not CONFIG_DIRECTORY:
        raise NotADirectoryError(f'Config directory not found. Environment path {CONFIG_ENV} does not seem to be set.')
    if name not in CONFIG_FILE_NAMES:
        raise FileNotFoundError(f'No config file with name "{name}" exists')
    path = CONFIG_DIRECTORY / name
    if not path.exists():
        raise FileNotFoundError(f'Could not find config file {name}')
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


if __name__ == '__main__':
    tran_name = get_translate_bvol_name_object()
    tran_size = get_translate_bvol_name_size_object()
    nomp = get_bvol_nomp_object()

