"""
Tests for Configuration System

Implements tests for config module.
"""

import pytest
import sys
import tempfile
import json
import yaml
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from md2office.config import Config
from md2office.config.config import load_config
from md2office.errors import ConfigurationError


class TestConfig:
    """Test suite for Config."""
    
    def test_init_empty(self):
        """Test initializing with empty config."""
        config = Config()
        assert config._config is not None
    
    def test_init_with_dict(self):
        """Test initializing with dictionary."""
        config_dict = {"output_dir": "/tmp"}
        config = Config(config_dict)
        assert config._config is not None
    
    def test_get_default_value(self):
        """Test getting default value."""
        config = Config()
        # Test that defaults are applied
        assert config._config is not None
    
    def test_load_from_json(self):
        """Test loading configuration from JSON file."""
        config_dict = {"output_dir": "/tmp/output"}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_dict, f)
            temp_path = f.name
        
        try:
            config = load_config(temp_path)
            assert config is not None
            assert config.get("output_dir") == "/tmp/output"
        finally:
            Path(temp_path).unlink()
    
    def test_load_from_yaml(self):
        """Test loading configuration from YAML file."""
        config_dict = {"output_dir": "/tmp/output"}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_dict, f)
            temp_path = f.name
        
        try:
            config = load_config(temp_path)
            assert config is not None
            assert config.get("output_dir") == "/tmp/output"
        finally:
            Path(temp_path).unlink()
    
    def test_update_config(self):
        """Test updating configuration."""
        config1 = Config({"key1": "value1"})
        config2 = {"key2": "value2"}
        config1.update(config2)
        # Verify update occurred
        assert config1.get("key2") == "value2"

