from typing import List

import pytest


def pytest_addoption(parser: pytest.Parser):
    parser.addoption(
        "--run-from-protobuf",
        action="store_true",
        default=False,
        help="Run from_protobuf() tests, network needed.",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: List[pytest.Item]):
    if config.getoption("--run-from-protobuf"):
        return

    from_protobuf = pytest.mark.skip(reason="--run-from-protobuf is False")
    for item in items:
        if "test_from_protobuf" in item.keywords:
            item.add_marker(from_protobuf)
