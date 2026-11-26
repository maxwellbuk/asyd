from configs.pydantic import ConfigPydantic

from pathlib import Path
import aiofiles.os

from pydantic import validate_call

class PacketDirs:

    @staticmethod
    @validate_call(config = ConfigPydantic.config_dict)
    async def create(
        dir: Path | str,
        dirs_exists_ok: bool | None = False
    ) -> None:
        try:
            await aiofiles.os.makedirs(
                dir,
                exist_ok = dirs_exists_ok
            )
        except FileExistsError:
            raise FileExistsError(f"Папка по пути: {dir}, уже существует")

    @staticmethod
    @validate_call(config = ConfigPydantic.config_dict)
    async def delete(
        dir: Path | str
    ) -> None:
        try:
            await aiofiles.os.removedirs(
                dir
            )
        except FileNotFoundError:
            raise FileNotFoundError(f"Папка по пути: {dir}, не существует")