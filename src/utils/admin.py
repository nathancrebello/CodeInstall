"""
Admin privilege management utilities.
"""
import sys
import ctypes
import logging

logger = logging.getLogger(__name__)


def is_admin() -> bool:
    """
    Check if the current process has administrator privileges.

    Returns:
        bool: True if running as administrator, False otherwise
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        logger.warning(f"Failed to check admin status: {e}")
        return False


def request_admin_privileges() -> None:
    """
    Request administrator privileges by relaunching the script with elevated permissions.

    Exits the current process if elevation is required.
    """
    if is_admin():
        logger.info("Already running with administrator privileges")
        return

    logger.info("Requesting administrator privileges...")
    try:
        script_path = sys.argv[0]
        params = ' '.join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            params,
            None,
            1
        )
        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to request admin privileges: {e}")
        raise
