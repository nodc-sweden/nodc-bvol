import functools
import pathlib

from nodc_config import Config

from nodc_bvol.bvol_nomp import BvolNomp
from nodc_bvol.translate_bvol_name import TranslateBvolName
from nodc_bvol.translate_bvol_name_size import TranslateBvolNameSize


def get_config_path(nodc_conf: Config, name: str) -> pathlib.Path:
    path = nodc_conf.get_path(name)
    if path is None:
        raise FileNotFoundError(f"nodc-config path '{name}' not found")
    return path


@functools.cache
def get_translate_bvol_name_object(nodc_conf: Config) -> "TranslateBvolName":
    path = get_config_path(nodc_conf, "translate_bvol_name.txt")
    return TranslateBvolName(path)


@functools.cache
def get_translate_bvol_name_size_object(nodc_conf: Config) -> "TranslateBvolNameSize":
    path = get_config_path(nodc_conf, "translate_bvol_name_size.txt")
    return TranslateBvolNameSize(path)


@functools.cache
def get_bvol_nomp_object(nodc_conf: Config) -> "BvolNomp":
    path = get_config_path(nodc_conf, "bvol_nomp.txt")
    return BvolNomp(path)
