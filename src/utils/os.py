from configs.pydantic import ConfigPydantic

from pathlib import Path
import aiofiles.os

from pydantic import validate_call

from typing import Literal

class PacketOS:

    @staticmethod
    @validate_call(config = ConfigPydantic.config_dict)
    async def check_existence_path(
        path: Path
    ) -> bool:
        return await aiofiles.os.path.exists(path)

    @staticmethod
    @validate_call(config = ConfigPydantic.config_dict)
    async def is_selected_type(
        path: Path,
        type: Literal["file", "dir"]
    ) -> bool:
        match type:
            case "file": return await aiofiles.os.path.isfile(path)
            case "dir": return await aiofiles.os.path.isdir(path)