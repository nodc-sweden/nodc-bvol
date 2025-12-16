import logging
import pathlib

import polars as pl

logger = logging.getLogger(__name__)


class TranslateBvolName:
    def __init__(self, path: str | pathlib.Path):
        self._path = pathlib.Path(path)
        self._df = None
        self._load_file()
        self._cleanup_data()

    @property
    def path(self) -> pathlib.Path:
        return self._path

    @property
    def source(self) -> str:
        return self.path.name

    def _load_file(self) -> None:
        self._df = pl.read_csv(self._path, separator="\t", encoding="cp1252")

    def _cleanup_data(self) -> None:
        self._df = self._df.filter(~pl.col("scientific_name_from").str.starts_with("#"))

    def get_scientific_name_from_to_mapper(self):
        return dict(
            zip(self._df["scientific_name_from"], self._df["scientific_name_to"])
        )

    def get(self, name: str) -> str | bool:
        """Returns the translated bvol name of the given name"""
        try:
            result = self._df.row(
                by_predicate=(pl.col("scientific_name_from") == name), named=True
            )["scientific_name_to"]
            # print(f'{result=}')
            if result:
                return result[0]
        except pl.exceptions.NoRowsReturnedError:
            return False
