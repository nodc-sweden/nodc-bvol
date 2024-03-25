import functools
import pathlib
import requests
import logging

from nodc_bvol.translate_bvol_name import TranslateBvolName
from nodc_bvol.translate_bvol_name_size import TranslateBvolNameSize
from nodc_bvol.bvol_nomp import BvolNomp


logger = logging.getLogger(__name__)


THIS_DIR = pathlib.Path(__file__).parent
CONFIG_DIR = THIS_DIR / 'CONFIG_FILES'

CONFIG_URLS = [
    r'https://raw.githubusercontent.com/nodc-sweden/nodc-bvol/main/src/nodc_bvol/CONFIG_FILES/bvol_nomp.txt',
    r'https://raw.githubusercontent.com/nodc-sweden/nodc-bvol/main/src/nodc_bvol/CONFIG_FILES/translate_bvol_name.txt',
    r'https://raw.githubusercontent.com/nodc-sweden/nodc-bvol/main/src/nodc_bvol/CONFIG_FILES/translate_bvol_name_size.txt',
]


@functools.cache
def get_translate_bvol_name_object() -> "TranslateBvolName":
    path = CONFIG_DIR / "translate_bvol_name.txt"
    return TranslateBvolName(path)


@functools.cache
def get_translate_bvol_name_size_object() -> "TranslateBvolNameSize":
    path = CONFIG_DIR / "translate_bvol_name_size.txt"
    return TranslateBvolNameSize(path)


@functools.cache
def get_translate_bvol_nomp_object() -> "BvolNomp":
    path = CONFIG_DIR / "bvol_nomp.txt"
    return BvolNomp(path)


def update_config_files() -> None:
    """Downloads config files from github"""
    try:
        for url in CONFIG_URLS:
            name = pathlib.Path(url).name
            target_path = CONFIG_DIR / name
            res = requests.get(url)
            with open(target_path, 'w', encoding='utf8') as fid:
                fid.write(res.text)
                logger.info(f'Config file "{name}" updated from {url}')
    except requests.exceptions.ConnectionError:
        logger.warning('Connection error. Could not update config files!')


if __name__ == '__main__':
    update_config_files()

