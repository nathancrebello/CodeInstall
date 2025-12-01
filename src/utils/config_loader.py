"""
Configuration loading and management utilities.
"""
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Handles loading and accessing configuration from YAML files."""

    def __init__(self, config_dir: Path):
        """
        Initialize the configuration loader.

        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = Path(config_dir)
        self._settings: Optional[Dict[str, Any]] = None
        self._applications: Optional[Dict[str, Any]] = None

    def load_settings(self) -> Dict[str, Any]:
        """
        Load general settings configuration.

        Returns:
            Dictionary containing settings
        """
        if self._settings is None:
            settings_file = self.config_dir / "settings.yaml"
            self._settings = self._load_yaml(settings_file)
        return self._settings

    def load_applications(self) -> Dict[str, Any]:
        """
        Load application definitions configuration.

        Returns:
            Dictionary containing application configurations
        """
        if self._applications is None:
            apps_file = self.config_dir / "applications.yaml"
            self._applications = self._load_yaml(apps_file)
        return self._applications

    def get_application_config(self, app_name: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for a specific application.

        Args:
            app_name: Name of the application (case-insensitive)

        Returns:
            Application configuration or None if not found
        """
        apps = self.load_applications()
        app_name_lower = app_name.lower()

        for key, config in apps.get('applications', {}).items():
            if key.lower() == app_name_lower:
                return config

        logger.warning(f"No configuration found for application: {app_name}")
        return None

    def _load_yaml(self, file_path: Path) -> Dict[str, Any]:
        """
        Load a YAML file.

        Args:
            file_path: Path to YAML file

        Returns:
            Parsed YAML content
        """
        try:
            if not file_path.exists():
                logger.warning(f"Configuration file not found: {file_path}")
                return {}

            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
                logger.info(f"Loaded configuration from {file_path}")
                return config
        except Exception as e:
            logger.error(f"Error loading configuration from {file_path}: {e}")
            return {}
