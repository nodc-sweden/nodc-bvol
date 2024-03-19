import logging
import pathlib
from typing import Tuple

import polars as pl

logger = logging.getLogger(__name__)


class BvolNomp:
    first_col = 'List'

    def __init__(self, path: str | pathlib.Path):
        self._path = pathlib.Path(path)
        self._df = None
        self._load_file()
        self._cleanup_data()

    def _load_file(self) -> None:
        self._df = pl.read_csv(self._path, separator='\t', encoding='cp1252', infer_schema_length=0)

    def _cleanup_data(self) -> None:
        self._df = self._df.filter(~pl.col(self.first_col).str.starts_with('#'))
        # self._df.columns = [col.lower() for col in self._df.columns]

    def get_info(self, **kwargs) -> dict | list | bool:
        """Returns information from nomp list filtered on data in kwargs"""
        data = self._df.filter(**kwargs).to_dict(as_series=False)
        info = []
        for i in range(len(data[self.first_col])):
            info.append(dict((key, data[key][i]) for key in data))
        if len(info) == 1:
            return info[0]
        return info
