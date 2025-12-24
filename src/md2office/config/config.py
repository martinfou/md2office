"""
Configuration System

Implements Story 1.5: Configuration System
Supports JSON and YAML configuration files.
"""

import json
import os
from typing import Dict, Any, Optional, List
from pathlib import Path
from ..errors import ConfigurationError


class Config:
    """
    Configuration manager for md2office.
    
    Supports loading from JSON/YAML files and merging with CLI options.
    """
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        """
        Initialize configuration.
        
        Args:
            config_dict: Initial configuration dictionary
        """
        self._config = config_dict or {}
        self._apply_defaults()
    
    def _apply_defaults(self):
        """Apply default configuration values."""
        defaults = get_default_config()
        
        # Merge defaults with current config
        for key, value in defaults.items():
            if key not in self._config:
                self._config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'output.directory')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def update(self, updates: Dict[str, Any]):
        """
        Update configuration with dictionary.
        
        Args:
            updates: Dictionary of updates
        """
        self._config.update(updates)
    
    def to_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary."""
        return self._config.copy()
    
    def get_output_formats(self) -> List[str]:
        """Get list of output formats from config."""
        formats = self.get('defaultFormats', [])
        if isinstance(formats, list):
            return formats
        return []
    
    def get_output_directory(self) -> str:
        """Get output directory from config."""
        return self.get('outputDirectory', '.')
    
    def get_style_preset(self) -> str:
        """Get style preset from config."""
        return self.get('style', 'default')
    
    def get_page_breaks(self) -> bool:
        """Get page breaks setting from config."""
        return self.get('pageBreaks', False)
    
    def get_table_of_contents(self) -> bool:
        """Get table of contents setting from config."""
        return self.get('tableOfContents', False)
    
    def get_image_optimization(self) -> str:
        """Get image optimization level from config."""
        return self.get('imageOptimization', 'medium')
    
    def get_overwrite(self) -> bool:
        """Get overwrite setting from config."""
        return self.get('overwrite', False)


def get_default_config() -> Dict[str, Any]:
    """
    Get default configuration.
    
    Returns:
        Default configuration dictionary
    """
    return {
        'defaultFormats': [],
        'outputDirectory': '.',
        'style': 'default',
        'pageBreaks': False,
        'tableOfContents': False,
        'bookmarks': True,
        'imageOptimization': 'medium',
        'overwrite': False,
        'verbose': False,
        'quiet': False,
        'continueOnError': False,
        'ignoreErrors': False
    }


def load_config(config_path: str) -> Config:
    """
    Load configuration from file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Config instance
        
    Raises:
        ConfigurationError: If file cannot be loaded or parsed
    """
    path = Path(config_path)
    
    if not path.exists():
        raise ConfigurationError(
            f"Configuration file not found: {config_path}",
            config_file=config_path
        )
    
    if not path.is_file():
        raise ConfigurationError(
            f"Configuration path is not a file: {config_path}",
            config_file=config_path
        )
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Determine file type by extension
        suffix = path.suffix.lower()
        
        if suffix == '.json':
            config_dict = json.loads(content)
        elif suffix in ['.yaml', '.yml']:
            try:
                import yaml
                config_dict = yaml.safe_load(content)
            except ImportError:
                raise ConfigurationError(
                    "YAML support requires PyYAML. Install with: pip install pyyaml",
                    config_file=config_path
                )
        else:
            # Try JSON first, then YAML
            try:
                config_dict = json.loads(content)
            except json.JSONDecodeError:
                try:
                    import yaml
                    config_dict = yaml.safe_load(content)
                except ImportError:
                    raise ConfigurationError(
                        "Could not parse configuration file. "
                        "Supported formats: JSON, YAML",
                        config_file=config_path
                    )
                except Exception as e:
                    raise ConfigurationError(
                        f"Error parsing YAML: {str(e)}",
                        config_file=config_path
                    )
        
        return Config(config_dict)
    
    except json.JSONDecodeError as e:
        raise ConfigurationError(
            f"Invalid JSON in configuration file: {str(e)}",
            config_file=config_path
        )
    except Exception as e:
        raise ConfigurationError(
            f"Error loading configuration file: {str(e)}",
            config_file=config_path
        )


def merge_configs(base_config: Config, override_config: Dict[str, Any]) -> Config:
    """
    Merge configuration with override values.
    
    CLI options override configuration file settings.
    
    Args:
        base_config: Base configuration
        override_config: Override values
        
    Returns:
        New Config instance with merged values
    """
    merged = base_config.to_dict()
    
    # Deep merge dictionaries
    def deep_merge(base: Dict, override: Dict):
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                deep_merge(base[key], value)
            else:
                base[key] = value
    
    deep_merge(merged, override_config)
    
    return Config(merged)


def find_config_file(start_path: Optional[str] = None) -> Optional[str]:
    """
    Find configuration file in directory hierarchy.
    
    Looks for .md2office.json, .md2office.yaml, or .md2office.yml
    in current directory and parent directories.
    
    Args:
        start_path: Starting directory path (defaults to current directory)
        
    Returns:
        Path to configuration file, or None if not found
    """
    if start_path is None:
        start_path = os.getcwd()
    
    path = Path(start_path).resolve()
    config_names = ['.md2office.json', '.md2office.yaml', '.md2office.yml']
    
    # Check current directory and parent directories
    for _ in range(10):  # Limit search depth
        for config_name in config_names:
            config_path = path / config_name
            if config_path.exists() and config_path.is_file():
                return str(config_path)
        
        # Move to parent directory
        parent = path.parent
        if parent == path:  # Reached filesystem root
            break
        path = parent
    
    return None

