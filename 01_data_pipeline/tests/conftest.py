import os
from pathlib import Path

def pytest_configure(config):
    os.chdir(Path(__file__).parent.parent.parent)