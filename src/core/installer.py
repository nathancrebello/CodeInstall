"""
Main installer automation logic.
"""
import os
import time
import logging
import subprocess
import urllib.request
from pathlib import Path
from typing import Optional, Dict, Any, Callable

from src.core.screen_automation import ScreenAutomation
from src.core.ai_assistant import AIAssistant

logger = logging.getLogger(__name__)


class InstallerAutomation:
    """Orchestrates the automated installation process."""

    def __init__(
        self,
        screen_automation: ScreenAutomation,
        ai_assistant: Optional[AIAssistant] = None,
        download_dir: Optional[Path] = None,
        ui_elements_dir: Optional[Path] = None,
        timeout: int = 10
    ):
        """
        Initialize the installer automation.

        Args:
            screen_automation: Screen automation instance
            ai_assistant: Optional AI assistant instance
            download_dir: Directory to save downloads (defaults to user's Downloads)
            ui_elements_dir: Directory containing UI element images
            timeout: Timeout for installer operations in seconds
        """
        self.screen = screen_automation
        self.ai = ai_assistant
        self.timeout = timeout

        self.download_dir = download_dir or Path.home() / "Downloads"
        self.ui_elements_dir = ui_elements_dir or Path("assets/ui_elements")

        logger.info("Installer automation initialized")

    def download_application(
        self,
        url: str,
        filename: str,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> Path:
        """
        Download an application installer.

        Args:
            url: Download URL
            filename: Filename to save as
            progress_callback: Optional callback for download progress

        Returns:
            Path to downloaded file
        """
        self.download_dir.mkdir(parents=True, exist_ok=True)
        file_path = self.download_dir / filename

        logger.info(f"Downloading from {url}")
        logger.info(f"Saving to {file_path}")

        try:
            if progress_callback:
                def reporthook(block_num, block_size, total_size):
                    downloaded = block_num * block_size
                    progress_callback(downloaded, total_size)

                urllib.request.urlretrieve(url, file_path, reporthook)
            else:
                urllib.request.urlretrieve(url, file_path)

            logger.info(f"Download completed: {file_path}")
            return file_path

        except Exception as e:
            logger.error(f"Download failed: {e}")
            raise

    def launch_installer(self, installer_path: Path, wait_time: int = 5) -> None:
        """
        Launch an installer executable.

        Args:
            installer_path: Path to installer file
            wait_time: Time to wait after launching (seconds)
        """
        if not installer_path.exists():
            raise FileNotFoundError(f"Installer not found: {installer_path}")

        logger.info(f"Launching installer: {installer_path}")
        os.startfile(str(installer_path))
        time.sleep(wait_time)

    def automate_installation(
        self,
        window_title: str,
        ui_elements_folder: str,
        status_callback: Optional[Callable[[str], None]] = None
    ) -> bool:
        """
        Automate the installation process using image recognition.

        Args:
            window_title: Title of the installer window
            ui_elements_folder: Folder containing UI element images
            status_callback: Optional callback for status updates

        Returns:
            True if installation completed successfully
        """
        try:
            # Find installer window
            installer_window = self.screen.find_window(window_title)
            if not installer_window:
                logger.error(f"Installer window not found: {window_title}")
                return False

            # Minimize other windows
            self.screen.minimize_other_windows([installer_window])

            # Get UI element images
            ui_folder = self.ui_elements_dir / ui_elements_folder
            image_paths = self.screen.get_image_paths(ui_folder)

            if not image_paths:
                logger.warning(f"No UI element images found in {ui_folder}")
                return False

            logger.info(f"Found {len(image_paths)} UI element images")

            # Automation loop
            last_click_time = time.time()

            while True:
                clicked = False

                # Try to find and click each UI element
                for image_path in image_paths:
                    if status_callback:
                        status_callback(f"Looking for: {image_path.name}")

                    location = self.screen.locate_image_on_screen(image_path)

                    if location:
                        self.screen.click_image_location(location)
                        last_click_time = time.time()
                        clicked = True
                        logger.info(f"Clicked: {image_path.name}")
                        time.sleep(1)  # Wait after click
                        break  # Start over from first image

                # Check timeout
                elapsed = time.time() - last_click_time
                if elapsed >= self.timeout:
                    logger.info(f"No clicks for {self.timeout}s, installation complete")
                    break

                if not clicked:
                    time.sleep(0.5)  # Small delay before next iteration

            if status_callback:
                status_callback("Installation completed")

            return True

        except Exception as e:
            logger.error(f"Error during installation automation: {e}")
            if status_callback:
                status_callback(f"Error: {e}")
            return False

    def install_with_ai(
        self,
        user_prompt: str,
        app_config: Dict[str, Any],
        status_callback: Optional[Callable[[str], None]] = None
    ) -> bool:
        """
        Install an application using AI-generated download script.

        Args:
            user_prompt: User's installation request
            app_config: Application configuration
            status_callback: Optional callback for status updates

        Returns:
            True if installation completed successfully
        """
        if not self.ai:
            logger.error("AI assistant not configured")
            return False

        try:
            # Generate download script
            if status_callback:
                status_callback("Generating download script...")

            code = self.ai.generate_download_script(user_prompt)
            if not code:
                logger.error("Failed to generate download script")
                return False

            # Extract and install required modules
            modules = self.ai.extract_required_modules(code)
            for module in modules:
                if status_callback:
                    status_callback(f"Installing module: {module}")
                try:
                    subprocess.run(
                        ['pip', 'install', module],
                        check=True,
                        capture_output=True
                    )
                except subprocess.CalledProcessError as e:
                    logger.warning(f"Failed to install {module}: {e}")

            # Execute download script
            if status_callback:
                status_callback("Downloading application...")

            subprocess.run(['python', '-c', code], check=True)
            time.sleep(5)  # Wait for installer to launch

            # Continue with automated installation
            return self.automate_installation(
                app_config['window_title_match'],
                app_config['ui_elements_folder'],
                status_callback
            )

        except Exception as e:
            logger.error(f"AI-assisted installation failed: {e}")
            if status_callback:
                status_callback(f"Error: {e}")
            return False

    def install_application(
        self,
        app_config: Dict[str, Any],
        status_callback: Optional[Callable[[str], None]] = None
    ) -> bool:
        """
        Install an application using predefined configuration.

        Args:
            app_config: Application configuration dictionary
            status_callback: Optional callback for status updates

        Returns:
            True if installation completed successfully
        """
        try:
            # Download installer
            if status_callback:
                status_callback("Downloading installer...")

            filename = f"{app_config['display_name']}_installer.{app_config['installer_extension']}"
            installer_path = self.download_application(
                app_config['download_url'],
                filename
            )

            # Launch installer
            if status_callback:
                status_callback("Launching installer...")

            self.launch_installer(installer_path)

            # Automate installation
            if status_callback:
                status_callback("Automating installation...")

            return self.automate_installation(
                app_config['window_title_match'],
                app_config['ui_elements_folder'],
                status_callback
            )

        except Exception as e:
            logger.error(f"Installation failed: {e}")
            if status_callback:
                status_callback(f"Error: {e}")
            return False
