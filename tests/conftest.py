from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def restore_activities_state():
    original_state = deepcopy(activities)

    yield

    activities.clear()
    activities.update(deepcopy(original_state))