import os
import shutil

import pytest

TOOLCHAIN = "leanprover/lean4:v4.33.1"


def _tc_bin():
    name = TOOLCHAIN.replace("/", "--").replace(":", "---")
    p = os.path.join(os.environ.get("ELAN_HOME", os.path.expanduser("~/.elan")), "toolchains", name, "bin")
    return p if os.path.exists(os.path.join(p, "lake")) else None


@pytest.fixture
def tc_bin():
    p = _tc_bin()
    if p is None:
        pytest.skip(f"{TOOLCHAIN} not installed")
    return p


@pytest.fixture
def tmp_project(tmp_path):
    return tmp_path / "proj"
