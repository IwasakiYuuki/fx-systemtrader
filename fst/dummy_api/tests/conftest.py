import os
import pytest

from dummy_api.api import app


@pytest.fixture
def client():
    """docstring for client"""
    app.config["TESTING"] = True
    
    with app.test_client() as client:
        yield client
