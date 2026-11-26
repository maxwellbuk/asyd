from utils.os import PacketOS

from configs.pydantic import ConfigPydantic

from pathlib import Path
import aiofiles

from typing import Literal

from pydantic import validate_call

class PacketFiles:

    @staticmethod
    @validate_call(config = ConfigPydantic.config_dict)
    async def record_value(
        value: str | bytes,
        file: Path | str,
        append: bool | None = False,
        exists_ok: bool | None = True
    ) -> None:
        if not exists_ok and await PacketOS.check_existence_path(file):
            raise FileExistsError(f"Файл, по пути: {file}, уже существует")

        match type(value).__name__:
            case "str": await _record_text(value, file, append)
            case "bytes": await _record_bytes(value, file, append)

    @staticmethod
    @validate_call(config = ConfigPydantic.config_dict)
    async def read_file(
        file: Path | str,
        mode: Literal["str", "bytes"]
    ) -> str | bytes:
        
        if not await PacketOS.check_existence_path(file):
            raise FileNotFoundError(f"По пути: {file}, не найден файл")

        if not await PacketOS.is_file(file):
            raise TypeError(f"Тип объекта: {file}, не является файлом")

        match mode:
            case "str": return await _read_text(file)
            case "bytes": return await _read_bytes(file)

async def _record_text(
    text: str,
    file: Path | str,
    append: bool | None = False
) -> None:
    async with aiofiles.open(
        file,
        "a" if append else "w",
        encoding = "utf-8"
    ) as current_file:
        await current_file.write(text)

async def _record_bytes(
    bytes: bytes,
    file: Path | str,
    append: bool | None = False
) -> None:
    async with aiofiles.open(
        file,
        "ab" if append else "wb"
    ) as current_file:
        await current_file.write(bytes)

async def _read_text(
    file: Path | str
) -> str:
    async with aiofiles.open(
        file,
        "r",
        encoding = "utf-8"
    ) as current_file:
        return await current_file.read()

async def _read_bytes(
    file: Path | str
) -> bytes:
    async with aiofiles.open(
        file,
        "rb"
    ) as current_file:
        return await current_file.read()