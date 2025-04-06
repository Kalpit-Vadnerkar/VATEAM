"""
Configuration Settings Module

This module handles all configuration settings for the CARLA driving toolkit.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class Settings:
    def __init__(self, config_path: Optional[str] = None):
        """Initialize settings from a config file.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = config_path
        self.settings = self._load_default_settings()
        
        if config_path:
            self.load_config(config_path)
            
    def _load_default_settings(self) -> Dict[str, Any]:
        """Load default settings."""
        return {
            'carla': {
                'host': 'localhost',
                'port': 2000,
                'timeout': 10.0,
                'vehicle_type': 'tesla.model3',
            },
            'sensors': {
                'rgb_camera': {
                    'location': [0.0, 0.0, 2.0],
                    'rotation': [0.0, 0.0, 0.0],
                    'fov': 90.0,
                },
                'lidar': {
                    'location': [0.0, 0.0, 2.5],
                    'rotation': [0.0, 0.0, 0.0],
                    'channels': 32,
                    'range': 50.0,
                }
            },
            'model': {
                'type': 'transfuser',
                'weights_path': 'model_ckpt/model.ckpt',
                'input_size': [224, 224],
                'batch_size': 1,
            },
            'visualization': {
                'enabled': True,
                'save_video': False,
                'output_dir': 'results',
            }
        }
        
    def load_config(self, config_path: str) -> None:
        """Load settings from a YAML file.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        with open(config_path, 'r') as f:
            user_settings = yaml.safe_load(f)
            
        # Update default settings with user settings
        self._update_dict(self.settings, user_settings)
        
    def _update_dict(self, d: Dict[str, Any], u: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively update a dictionary.
        
        Args:
            d: Base dictionary
            u: Update dictionary
            
        Returns:
            Updated dictionary
        """
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = self._update_dict(d.get(k, {}), v)
            else:
                d[k] = v
        return d
        
    def save_config(self, config_path: Optional[str] = None) -> None:
        """Save current settings to a YAML file.
        
        Args:
            config_path: Path to save the configuration file
        """
        save_path = config_path or self.config_path
        if save_path is None:
            raise ValueError("No config path specified")
            
        with open(save_path, 'w') as f:
            yaml.dump(self.settings, f, default_flow_style=False)
            
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value by key.
        
        Args:
            key: Setting key (dot notation supported)
            default: Default value if key not found
            
        Returns:
            Setting value
        """
        keys = key.split('.')
        value = self.settings
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
                
        return value if value is not None else default 