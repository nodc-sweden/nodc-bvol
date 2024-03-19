import logging
import pathlib
from typing import Tuple

import polars as pl

logger = logging.getLogger(__name__)


class TranslateBvolName:

    def __init__(self, path: str | pathlib.Path):
        self._path = pathlib.Path(path)
        self._df = None
        self._load_file()
        self._cleanup_data()

    def _load_file(self) -> None:
        self._df = pl.read_csv(self._path, separator='\t', encoding='cp1252')

    def _cleanup_data(self) -> None:
        self._df = self._df.filter(~pl.col('scientific_name_from').str.starts_with('#'))

    def get(self, name: str) -> str | bool:
        """Returns the translated bvol name of the given name"""
        try:
            return self._df.row(by_predicate=(pl.col('scientific_name_from') == name), named=True)['scientific_name_to']
        except pl.exceptions.NoRowsReturnedError:
            return False
