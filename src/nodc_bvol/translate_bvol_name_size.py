import logging
import pathlib
from typing import Tuple

import polars as pl

logger = logging.getLogger(__name__)


class TranslateBvolNameSize:

    def __init__(self, path: str | pathlib.Path):
        self._path = pathlib.Path(path)
        self._df = None
        self._load_file()
        self._cleanup_data()

    def _load_file(self) -> None:
        self._df = pl.read_csv(self._path, separator='\t', encoding='utf8')

    def _cleanup_data(self) -> None:
        self._df = self._df.filter(~pl.col('scientific_name_from').str.starts_with('#'))

    def get(self, name: str, size: str | int) -> Tuple[str, str] | bool:
        """Returns the translated bvol name and size of the given name and size"""
        size = int(size)
        try:
            data = self._df.row(by_predicate=((pl.col('scientific_name_from') == name) & (pl.col('size_class_from') == size)), named=True)
            return data['scientific_name_to'], data['size_class_to']
        except pl.exceptions.NoRowsReturnedError:
            return False
