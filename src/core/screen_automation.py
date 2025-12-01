"""
Screen automation using computer vision and GUI automation.
"""
import time
import logging
from pathlib import Path
from typing import Optional, Tuple, List

import pyautogui
import pygetwindow as gw
import pytesseract as tess
from PIL import Image, ImageGrab
from pywinauto import Desktop

logger = logging.getLogger(__name__)


class ScreenAutomation:
    """Handles screen automation, window management, and image detection."""

    def __init__(
        self,
        tesseract_path: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        mouse_duration: float = 0.5
    ):
        """
        Initialize screen automation.

        Args:
            tesseract_path: Path to Tesseract OCR executable
            max_retries: Maximum number of retries for image detection
            retry_delay: Delay between retries in seconds
            mouse_duration: Duration of mouse movements in seconds
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.mouse_duration = mouse_duration

        if tesseract_path:
            tess.pytesseract.tesseract_cmd = tesseract_path
            logger.info(f"Tesseract path set to: {tesseract_path}")

    def find_window(self, title_match: str) -> Optional[str]:
        """
        Find a window by title substring match.

        Args:
            title_match: Substring to match in window title

        Returns:
            Full window title if found, None otherwise
        """
        all_windows = gw.getAllTitles()
        matching_windows = [title for title in all_windows if title_match in title]

        if matching_windows:
            logger.info(f"Found window: {matching_windows[0]}")
            return matching_windows[0]

        logger.warning(f"No window found matching: {title_match}")
        return None

    def minimize_other_windows(self, keep_windows: List[str]) -> None:
        """
        Minimize all windows except those in the keep list.

        Args:
            keep_windows: List of window titles to keep open
        """
        for window_title in gw.getAllTitles():
            if window_title not in keep_windows:
                try:
                    window = gw.getWindowsWithTitle(window_title)[0]
                    window.minimize()
                except (IndexError, Exception) as e:
                    logger.debug(f"Could not minimize window '{window_title}': {e}")

    def locate_image_on_screen(
        self,
        image_path: Path,
        confidence: float = 0.8
    ) -> Optional[Tuple[int, int, int, int]]:
        """
        Locate an image on the screen with retries.

        Args:
            image_path: Path to the image file to locate
            confidence: Matching confidence (0-1)

        Returns:
            Tuple of (left, top, width, height) if found, None otherwise
        """
        logger.debug(f"Searching for image: {image_path}")

        for attempt in range(self.max_retries):
            try:
                location = pyautogui.locateOnScreen(
                    str(image_path),
                    confidence=confidence
                )
                if location:
                    logger.info(f"Found image: {image_path}")
                    return location
            except pyautogui.ImageNotFoundException:
                pass
            except Exception as e:
                logger.error(f"Error locating image {image_path}: {e}")

            if attempt < self.max_retries - 1:
                time.sleep(self.retry_delay)

        logger.debug(f"Image not found after {self.max_retries} attempts: {image_path}")
        return None

    def click_image_location(
        self,
        location: Tuple[int, int, int, int],
        offset_x: int = 0,
        offset_y: int = 0
    ) -> None:
        """
        Click at the center of an image location.

        Args:
            location: Tuple of (left, top, width, height)
            offset_x: X offset from center
            offset_y: Y offset from center
        """
        left, top, width, height = location
        center_x = left + width / 2 + offset_x
        center_y = top + height / 2 + offset_y

        pyautogui.moveTo(center_x, center_y, duration=self.mouse_duration)
        pyautogui.click()

        # Move mouse slightly away to avoid hover effects
        pyautogui.moveTo(center_x + 50, center_y + 50, duration=0.1)
        logger.info(f"Clicked at position ({center_x}, {center_y})")

    def capture_window_screenshot(self, window_title: str) -> Optional[Image.Image]:
        """
        Capture a screenshot of a specific window.

        Args:
            window_title: Title of the window to capture

        Returns:
            PIL Image object or None if window not found
        """
        try:
            windows = gw.getWindowsWithTitle(window_title)
            if not windows:
                logger.warning(f"Window not found: {window_title}")
                return None

            window = windows[0]
            bbox = (window.left, window.top, window.right, window.bottom)
            screenshot = ImageGrab.grab(bbox=bbox)
            return screenshot
        except Exception as e:
            logger.error(f"Error capturing window screenshot: {e}")
            return None

    def compare_screenshots(self, img1: Image.Image, img2: Image.Image) -> bool:
        """
        Compare two screenshots using OCR text extraction.

        Args:
            img1: First image
            img2: Second image

        Returns:
            True if images have same text content, False otherwise
        """
        try:
            text1 = tess.image_to_string(img1)
            text2 = tess.image_to_string(img2)
            return text1 == text2
        except Exception as e:
            logger.error(f"Error comparing screenshots: {e}")
            return False

    def get_image_paths(self, folder_path: Path, pattern: str = "*") -> List[Path]:
        """
        Get all image file paths from a folder recursively.

        Args:
            folder_path: Root folder to search
            pattern: Optional pattern to filter files

        Returns:
            List of image file paths
        """
        if not folder_path.exists():
            logger.warning(f"Folder not found: {folder_path}")
            return []

        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
        image_paths = []

        for file_path in folder_path.rglob('*'):
            if file_path.suffix.lower() in image_extensions:
                if pattern == "*" or pattern.lower() in str(file_path).lower():
                    image_paths.append(file_path)

        logger.info(f"Found {len(image_paths)} images in {folder_path}")
        return image_paths
