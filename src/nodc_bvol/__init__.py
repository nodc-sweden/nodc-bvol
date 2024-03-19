import functools
import pathlib
import sys

from .translate_bvol_name import TranslateBvolName
from .translate_bvol_name_size import TranslateBvolNameSize
from .bvol_nomp import BvolNomp


if getattr(sys, 'frozen', False):
    THIS_DIR = pathlib.Path(sys.executable).parent
else:
    THIS_DIR = pathlib.Path(__file__).parent

CONFIG_DIR = THIS_DIR.parent / 'CONFIG_FILES'

if not CONFIG_DIR.exists():
    CONFIG_DIR = THIS_DIR / 'CONFIG_FILES'


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


