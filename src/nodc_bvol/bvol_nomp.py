import functools
import logging
import pathlib

import numpy as np
import polars as pl

logger = logging.getLogger(__name__)


class BvolNomp:
    first_col = "List"

    def __init__(self, path: str | pathlib.Path):
        self._path = pathlib.Path(path)
        self._df: pl.DataFrame = None
        self._load_file()
        self._cleanup_data()
        self._add_joined_column()

    @property
    def path(self) -> pathlib.Path:
        return self._path

    @property
    def source(self) -> str:
        return self.path.name

    def _load_file(self) -> None:
        self._df = pl.read_csv(
            self._path, separator="\t", encoding="cp1252", infer_schema_length=0
        )

    def _cleanup_data(self) -> None:
        self._df = self._df.filter(~pl.col(self.first_col).str.starts_with("#"))

    def _add_joined_column(self):
        self._df = self._df.with_columns(
            pl.concat_str(
                [
                    pl.col("Species"),
                    pl.col("SizeClassNo"),
                ],
                separator=":",
            ).alias("species_and_size_class")
        )

    def get_info(self, **kwargs) -> dict | list | bool:
        """Returns information from nomp list filtered on data in kwargs"""
        data = self._df.filter(**kwargs).to_dict(as_series=False)
        info = []
        for i in range(len(data[self.first_col])):
            info.append(dict((key, data[key][i]) for key in data))
        if len(info) == 1:
            return info[0]
        return info

    @functools.cache
    def get_species_to_aphia_id_mapper(self):
        df = self._df.filter(pl.col("AphiaID") != "")
        return dict(zip(df["Species"], df["AphiaID"]))

    @functools.cache
    def get_species_and_size_class_to_aphia_id_mapper(self):
        return dict(zip(self._df["species_and_size_class"], self._df["AphiaID"]))

    @functools.cache
    def get_species_and_size_class_to_ref_list_mapper(self):
        return dict(zip(self._df["species_and_size_class"], self._df["List"]))

    @functools.cache
    def get_calculated_volume_mapper(self):
        mapping = {}
        for (aphia_id, size_class), df in self._df.group_by(["AphiaID", "SizeClassNo"]):
            value = df["Calculated_volume_µm3"][0].replace(",", ".").strip()
            if value:
                value = float(value)  # * 10e-9
            else:
                value = np.nan
            if aphia_id is None:
                aphia_id = ""
            mapping[":".join((aphia_id, size_class))] = value
        return mapping

    @functools.cache
    def get_carbon_per_volume_mapper(self):
        mapping = {}
        for (aphia_id, size_class), df in self._df.group_by(["AphiaID", "SizeClassNo"]):
            value = (
                df["Calculated_Carbon_pg/counting_unit"][0].replace(",", ".").strip()
            )
            if value:
                value = float(value) / 1_000_000
            else:
                value = np.nan
            if aphia_id is None:
                aphia_id = ""
            mapping[":".join((aphia_id, size_class))] = value
        return mapping
