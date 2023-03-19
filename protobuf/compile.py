import os
import re
import shutil
from pathlib import Path
from typing import Dict

DIRNAME = Path(Path(__file__).parent)

PROTOBUF_SOURCE_ROOT_DIR = DIRNAME / "source"
PROTOBUF_SOURCE_DIRS = [
    PROTOBUF_SOURCE_ROOT_DIR / "common",
    PROTOBUF_SOURCE_ROOT_DIR / "request",
    PROTOBUF_SOURCE_ROOT_DIR / "response",
]
PROTOBUF_IMPORT_DIRS = [
    PROTOBUF_SOURCE_ROOT_DIR / "common",
]
PROTOBUF_OUT_DIR = DIRNAME / "out"
PROTOBUF_FINAL_DIR = (
    DIRNAME / ".." / "src" / "tieba_thread_archive" / "remote" / "protobuf"
)

PROTOC = "protoc"

detect_protoc = os.popen(PROTOC).read()
for expect_output in ["protoc", "--python_out=", "--pyi_out="]:
    if expect_output not in detect_protoc:
        print("protoc not found or version too low.")
        print(
            "Requires protoc >= 3.20.0 (2022-03-25), which supports generating pyi stub files."
        )
        exit(1)

# register protobufs
protobuf_name_reldir: Dict[str, str] = {}
for source_dir in PROTOBUF_SOURCE_DIRS:
    for file in source_dir.iterdir():
        if file.match("*.proto"):
            protobuf_name_reldir[file.stem] = str(
                source_dir.relative_to(PROTOBUF_SOURCE_ROOT_DIR)
            )


def add_init_py(path: Path):
    with open(path / "__init__.py", "w") as f:
        f.write("")


if PROTOBUF_FINAL_DIR.exists():
    shutil.rmtree(PROTOBUF_FINAL_DIR)
os.makedirs(PROTOBUF_FINAL_DIR, exist_ok=True)
add_init_py(PROTOBUF_FINAL_DIR)

# compile
for source_dir in PROTOBUF_SOURCE_DIRS:
    relative_dir = source_dir.relative_to(PROTOBUF_SOURCE_ROOT_DIR)
    target_dir = PROTOBUF_OUT_DIR / relative_dir
    os.makedirs(target_dir, exist_ok=True)
    add_init_py(target_dir)

    command_segments = [
        PROTOC,
        *[f"-I {idir}/" for idir in PROTOBUF_SOURCE_DIRS],
        f"--python_out={target_dir}",
        f"--pyi_out={target_dir}",
        str(source_dir / "*.proto"),
    ]

    os.popen(" ".join(command_segments)).read()

    # fix import statements
    for file in target_dir.iterdir():
        if re.match(r".*\.pyi?", file.name):
            with open(file, "r+", encoding="utf-8") as f:
                content = f.read()
                content.replace("\r\n", "\n")
                pb_imports = re.findall(r"import (.*)_pb2 as", content)
                for pb_import in pb_imports:
                    register_relative_dir = protobuf_name_reldir[pb_import]
                    content = content.replace(
                        f"import {pb_import}_pb2 as",
                        f"from . import {pb_import}_pb2 as"
                        if register_relative_dir == str(relative_dir)
                        else f"from ..{register_relative_dir} import {pb_import}_pb2 as",
                    )
                f.seek(0)
                f.truncate()
                f.write(content)

    shutil.move(target_dir, PROTOBUF_FINAL_DIR)
