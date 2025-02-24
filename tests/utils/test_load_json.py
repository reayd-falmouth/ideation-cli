import json
import pytest
from ideation_cli import utils

pytestmark = pytest.mark.unit


def test_load_json(tmp_path):
    # Create a temporary JSON file.
    data = {"key": "value", "number": 123}
    file_path = tmp_path / "test.json"
    file_path.write_text(json.dumps(data))

    # Call load_json and verify the output matches the original data.
    loaded = utils.load_json(str(file_path))
    assert loaded == data
