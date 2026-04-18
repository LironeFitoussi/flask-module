from pathlib import Path
import sys

import pytest

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from app import app  # noqa: E402
from db import get_collection  # noqa: E402


@pytest.fixture(autouse=True)
def clean_db():
    get_collection("tasks").delete_many({})
    get_collection("lists").delete_many({})
    yield
    get_collection("tasks").delete_many({})
    get_collection("lists").delete_many({})


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client
