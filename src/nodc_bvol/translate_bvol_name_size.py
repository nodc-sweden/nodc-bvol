import functools
import logging
import pathlib

import polars as pl

logger = logging.getLogger(__name__)


class TranslateBvolNameSize:
    def __init__(self, path: str | pathlib.Path):
        self._path = pathlib.Path(path)
        self._df: pl.DataFrame | None = None
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

    def _get_return_data(self, data: dict) -> dict:
        return dict(
            name=data.get("scientific_name_to", ""),
            size_class=data.get("size_class_to", ""),
        )

    def _get_translated_name_only(self, name: str) -> dict:
        try:
            data = self._df.filter(pl.col("scientific_name_from") == name).to_dicts()
            if not data:
                return dict()
            d = data[0]
            d.pop("size_class_to")
            return self._get_return_data(d)
        except pl.exceptions.NoRowsReturnedError:
            return dict()

    def get(self, name: str, size: str | int = None) -> dict:
        """Returns the translated bvol name and size of the given name and size"""
        if not size:
            return self._get_translated_name_only(name)
        size = int(size)
        try:
            data = self._df.row(
                by_predicate=(
                    (pl.col("scientific_name_from") == name)
                    & (pl.col("size_class_from") == size)
                ),
                named=True,
            )
            return self._get_return_data(data)
        except pl.exceptions.NoRowsReturnedError:
            return self._get_translated_name_only(name)

    @functools.cache
    def get_scientific_name_from_to_mapper(self) -> dict:
        df = self._df.with_columns(
            pl.concat_str(
                [pl.col("scientific_name_from"), pl.col("size_class_from")],
                separator=":",
            ).alias("combined_from"),
            pl.concat_str(
                [pl.col("scientific_name_to"), pl.col("size_class_to")], separator=":"
            ).alias("combined_to"),
            pl.concat_str(
                [pl.col("scientific_name_from"), pl.lit("")], separator=":"
            ).alias("combined_from_only_scientific_name"),
            pl.concat_str(
                [pl.col("scientific_name_to"), pl.lit("")], separator=":"
            ).alias("combined_to_only_scientific_name"),
        )
        data = dict(zip(df["combined_from"], df["combined_to"]))
        data.update(
            dict(
                zip(
                    df["combined_from_only_scientific_name"],
                    df["combined_to_only_scientific_name"],
                )
            )
        )
        return data
