import json
import os
import pytest
from ideation_cli import utils

pytestmark = pytest.mark.unit


def test_save_args_to_json(tmp_path):
    data = {"foo": "bar", "count": 10}
    # Create a temporary directory to save the JSON file.
    dir_path = tmp_path / "test_dir"
    dir_path.mkdir()
    utils.save_args_to_json(data, str(dir_path))

    json_file = os.path.join(str(dir_path), "metadata.json")
    assert os.path.exists(json_file)
    with open(json_file, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded == data
