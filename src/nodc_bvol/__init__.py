import functools
import os
import pathlib
import ssl

import requests
import logging

from nodc_bvol.translate_bvol_name import TranslateBvolName
from nodc_bvol.translate_bvol_name_size import TranslateBvolNameSize
from nodc_bvol.bvol_nomp import BvolNomp


logger = logging.getLogger(__name__)

CONFIG_SUBDIRECTORY = 'nodc_bvol'
CONFIG_FILE_NAMES = [
    'bvol_nomp.txt',
    'translate_bvol_name.txt',
    'translate_bvol_name_size.txt',
]


CONFIG_DIRECTORY = None
if os.getenv('NODC_CONFIG'):
    CONFIG_DIRECTORY = pathlib.Path(os.getenv('NODC_CONFIG')) / CONFIG_SUBDIRECTORY
TEMP_CONFIG_DIRECTORY = pathlib.Path.home() / 'temp_nodc_config' / CONFIG_SUBDIRECTORY


CONFIG_URL = r'https://raw.githubusercontent.com/nodc-sweden/nodc_config/refs/heads/main/' + f'{CONFIG_SUBDIRECTORY}/'


def get_config_path(name: str) -> pathlib.Path:
    if name not in CONFIG_FILE_NAMES:
        raise FileNotFoundError(f'No config file with name "{name}" exists')
    if CONFIG_DIRECTORY:
        path = CONFIG_DIRECTORY / name
        if path.exists():
            return path
    temp_path = TEMP_CONFIG_DIRECTORY / name
    if temp_path.exists():
        return temp_path
    update_config_file(temp_path)
    if temp_path.exists():
        return temp_path
    raise FileNotFoundError(f'Could not find config file {name}')


def update_config_file(path: pathlib.Path) -> None:
    path.parent.mkdir(exist_ok=True, parents=True)
    url = CONFIG_URL + path.name
    try:
        res = requests.get(url, verify=ssl.CERT_NONE)
        with open(path, 'w', encoding='utf8') as fid:
            fid.write(res.text)
            logger.info(f'Config file "{path.name}" updated from {url}')
    except requests.exceptions.ConnectionError:
        logger.warning(f'Connection error. Could not update config file {path.name}')
        raise


def update_config_files() -> None:
    """Downloads config files from github"""
    for name in CONFIG_FILE_NAMES:
        target_path = TEMP_CONFIG_DIRECTORY / name
        update_config_file(target_path)


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
    update_config_files()

