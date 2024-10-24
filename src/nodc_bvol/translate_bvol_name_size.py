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

    def _get_return_data(self, data: dict) -> dict:
        return dict(
            name=data.get('scientific_name_to', ''),
            size_class=data.get('size_class_to', ''),
        )

    def _get_translated_name_only(self, name: str) -> dict:
        try:
            data = self._df.filter(pl.col('scientific_name_from') == name).to_dicts()
            if not data:
                return dict()
            d = data[0]
            d.pop('size_class_to')
            return self._get_return_data(d)
        except pl.exceptions.NoRowsReturnedError:
            return dict()

    def get(self, name: str, size: str | int = None) -> dict:
        """Returns the translated bvol name and size of the given name and size"""
        if not size:
            return self._get_translated_name_only(name)
        size = int(size)
        try:
            data = self._df.row(by_predicate=((pl.col('scientific_name_from') == name) & (pl.col('size_class_from') == size)), named=True)
            return self._get_return_data(data)
        except pl.exceptions.NoRowsReturnedError:
            return self._get_translated_name_only(name)
