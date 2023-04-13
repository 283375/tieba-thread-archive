from typing import List

import pytest


def pytest_addoption(parser: pytest.Parser):
    parser.addoption(
        "--run-from-protobuf",
        action="store_true",
        default=False,
        help="Run from_protobuf() tests, network needed.",
    )
    parser.addoption(
        "--file-sensitive",
        action="store_true",
        default=False,
        help="Run file sensitive tests."
        " These tests may result in data loss or file damage,"
        "be sure to backup your files under `__debug_tests` before proceeding.",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: List[pytest.Item]):
    if not config.getoption("--run-from-protobuf"):
        from_protobuf = pytest.mark.skip(reason="--run-from-protobuf is False")
        for item in items:
            if "test_from_protobuf" in item.keywords:
                item.add_marker(from_protobuf)

    if not config.getoption("--file-sensitive"):
        file_sensitive = pytest.mark.skip(reason="--file-sensitive is False")
        for item in items:
            if ("file_sensitive" in item.keywords) or (
                item.parent and "FileSensitive" in item.parent.name
            ):
                item.add_marker(file_sensitive)
