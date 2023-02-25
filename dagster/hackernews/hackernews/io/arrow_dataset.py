from typing import Union
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
from pyarrow.fs import FileSystem, LocalFileSystem, S3FileSystem

from dagster import Any, IOManager, InputContext, OutputContext, io_manager
from dagster import (
    Field,
    InputContext,
    DagsterInvalidConfigError,
    OutputContext,
    StringSource,
    _check as check,
    io_manager,
)
from sqlalchemy import Sequence


class ArrowDataSetIO(IOManager):
    def __init__(self, 
                filesystem: FileSystem,
                prefix: str) -> None:
        self.filesystem = filesystem
        self.prefix = prefix
        super().__init__()

    def _get_configured_filesystem() -> "FileSystem":
        """
        Get Arrow file system related to running environment
        """
        # todo    

    def _get_stored_path(self, context: Union[InputContext, OutputContext]) -> str:
        path: Sequence[str]
        if context.has_asset_key:
            path = context.get_asset_identifier()
        else:
            path = ["storage", *context.get_identifier()]

        return "/".join([self.prefix,*path])
        
    def load_input(self, context: "InputContext") -> Any:
        context.log.info(vars(context.upstream_output))
        file_format = context.upstream_output.metadata['stored_as']
        context.log.info(f"Stored format: {file_format}")
        if file_format == "parquet":
            data_path = self._get_stored_path(context=context)
            data = pq.ParquetDataset(
                path_or_paths=data_path,
                filesystem=self.filesystem
            )
            return data

    def handle_output(self, context: "OutputContext", obj: Any) -> None:
        context.log.info(vars(context))
        if isinstance(obj, pd.DataFrame):
            file_format =context.metadata.get("stored_as")
            # context.log.info(f"File format: {file_format}")
            if file_format == 'parquet':
                data_path = f"{self._get_stored_path(context=context)}"
                context.log.info(data_path)
                table = pa.Table.from_pandas(obj)
                pq.write_to_dataset(
                    table, 
                    root_path=data_path, 
                    filesystem=self.filesystem
                )
                context.log.info(f"Path: {data_path}")
        return super().handle_output(context, obj)

@io_manager(
    config_schema={
        "filesystem": Field(StringSource),
        "endpoint_url": Field(StringSource),
        "prefix": Field(StringSource, is_required=False, default_value="dagster")
    }
)
def arrow_dataset_io(init_context) -> ArrowDataSetIO:
    
    configured_filesystem = init_context.resource_config.get("filesystem")
    if configured_filesystem == "LocalFileSystem":
        filesystem = LocalFileSystem()
    elif configured_filesystem == "S3FileSystem":
        filesystem = S3FileSystem(
            endpoint_override=init_context.resource_config.get("endpoint_url")
        )
    else:
        raise DagsterInvalidConfigError(
            errors="The configured filesystem {} is not supporterd".format(filesystem)
        )
    prefix = init_context.resource_config["prefix"]
    arrow_io_manager = ArrowDataSetIO(
        filesystem=filesystem,
        prefix=prefix
    )
    return arrow_io_manager