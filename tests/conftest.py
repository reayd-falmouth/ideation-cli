import os
import pytest


@pytest.fixture
def openai_env():
    os.environ["OPENAI_API_KEY"] = "somekey"
