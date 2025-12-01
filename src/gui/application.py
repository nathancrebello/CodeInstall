"""
GUI application for the installer automation tool.
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import logging
from pathlib import Path
from typing import Optional, Dict, Any

from src.core.installer import InstallerAutomation
from src.utils.config_loader import ConfigLoader

logger = logging.getLogger(__name__)


class InstallerGUI:
    """Main GUI application for installer automation."""

    def __init__(
        self,
        installer: InstallerAutomation,
        config_loader: ConfigLoader,
        settings: Dict[str, Any]
    ):
        """
        Initialize the GUI application.

        Args:
            installer: InstallerAutomation instance
            config_loader: ConfigLoader instance
            settings: Application settings dictionary
        """
        self.installer = installer
        self.config_loader = config_loader
        self.settings = settings

        # Create main window
        self.root = tk.Tk()
        self.root.title(settings['gui']['title'])
        self.root.geometry(
            f"{settings['gui']['window_width']}x{settings['gui']['window_height']}"
        )
        self.root.configure(bg=settings['gui']['theme'])

        self._setup_ui()
        logger.info("GUI initialized")

    def _setup_ui(self) -> None:
        """Setup the user interface."""
        # Title label
        title_label = tk.Label(
            self.root,
            text="Installer Automation Tool",
            font=("Arial", 16, "bold"),
            bg=self.settings['gui']['theme'],
            fg="white"
        )
        title_label.pack(pady=20)

        # Subtitle
        subtitle_label = tk.Label(
            self.root,
            text="Automate software installation with AI and computer vision",
            bg=self.settings['gui']['theme'],
            fg="lightgray"
        )
        subtitle_label.pack(pady=5)

        # Main container
        main_frame = tk.Frame(self.root, bg=self.settings['gui']['theme'])
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Install section
        self._create_install_section(main_frame)

        # Open section
        self._create_open_section(main_frame)

        # Status section
        self._create_status_section(main_frame)

    def _create_install_section(self, parent: tk.Frame) -> None:
        """Create the installation section."""
        section = tk.LabelFrame(
            parent,
            text="Download & Install Application",
            bg=self.settings['gui']['theme'],
            fg="white",
            font=("Arial", 10, "bold")
        )
        section.pack(fill=tk.X, pady=10)

        # Input frame
        input_frame = tk.Frame(section, bg=self.settings['gui']['theme'])
        input_frame.pack(pady=10, padx=10, fill=tk.X)

        # Application dropdown
        tk.Label(
            input_frame,
            text="Select Application:",
            bg=self.settings['gui']['theme'],
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

        apps = self.config_loader.load_applications()
        app_names = list(apps.get('applications', {}).keys())

        self.app_var = tk.StringVar()
        self.app_dropdown = ttk.Combobox(
            input_frame,
            textvariable=self.app_var,
            values=app_names,
            state="readonly",
            width=20
        )
        self.app_dropdown.pack(side=tk.LEFT, padx=5)
        if app_names:
            self.app_dropdown.current(0)

        # Install button
        self.install_button = tk.Button(
            input_frame,
            text="Install",
            command=self._on_install_click,
            bg="green",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        )
        self.install_button.pack(side=tk.LEFT, padx=10)

        # Custom input section
        custom_frame = tk.Frame(section, bg=self.settings['gui']['theme'])
        custom_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(
            custom_frame,
            text="Or enter custom request:",
            bg=self.settings['gui']['theme'],
            fg="white"
        ).pack(anchor=tk.W)

        self.custom_input = tk.Entry(custom_frame, width=50)
        self.custom_input.pack(pady=5, fill=tk.X)
        self.custom_input.insert(0, "Download Python")

        self.custom_button = tk.Button(
            custom_frame,
            text="Install with AI",
            command=self._on_custom_install_click,
            bg="blue",
            fg="white",
            width=12
        )
        self.custom_button.pack(pady=5)

    def _create_open_section(self, parent: tk.Frame) -> None:
        """Create the application launcher section."""
        section = tk.LabelFrame(
            parent,
            text="Open Installed Application",
            bg=self.settings['gui']['theme'],
            fg="white",
            font=("Arial", 10, "bold")
        )
        section.pack(fill=tk.X, pady=10)

        input_frame = tk.Frame(section, bg=self.settings['gui']['theme'])
        input_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(
            input_frame,
            text="Application name:",
            bg=self.settings['gui']['theme'],
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

        self.open_input = tk.Entry(input_frame, width=30)
        self.open_input.pack(side=tk.LEFT, padx=5)

        self.open_button = tk.Button(
            input_frame,
            text="Open",
            command=self._on_open_click,
            bg="orange",
            fg="white",
            width=12
        )
        self.open_button.pack(side=tk.LEFT, padx=10)

    def _create_status_section(self, parent: tk.Frame) -> None:
        """Create the status display section."""
        section = tk.LabelFrame(
            parent,
            text="Status",
            bg=self.settings['gui']['theme'],
            fg="white",
            font=("Arial", 10, "bold")
        )
        section.pack(fill=tk.BOTH, expand=True, pady=10)

        # Status text area
        self.status_text = scrolledtext.ScrolledText(
            section,
            height=10,
            bg="black",
            fg="lightgreen",
            font=("Consolas", 9)
        )
        self.status_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.status_text.insert("1.0", "Ready to install applications...\n")
        self.status_text.config(state=tk.DISABLED)

    def _update_status(self, message: str) -> None:
        """
        Update the status display.

        Args:
            message: Status message to display
        """
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update()
        logger.info(message)

    def _on_install_click(self) -> None:
        """Handle install button click."""
        app_name = self.app_var.get()
        if not app_name:
            messagebox.showwarning("No Selection", "Please select an application")
            return

        self._disable_buttons()
        self._update_status(f"Starting installation of {app_name}...")

        try:
            app_config = self.config_loader.get_application_config(app_name)
            if not app_config:
                raise ValueError(f"Configuration not found for {app_name}")

            success = self.installer.install_application(
                app_config,
                status_callback=self._update_status
            )

            if success:
                self._update_status(f"✓ {app_name} installed successfully!")
                messagebox.showinfo("Success", f"{app_name} installed successfully!")
            else:
                self._update_status(f"✗ Installation of {app_name} failed")
                messagebox.showerror("Error", "Installation failed. Check logs for details.")

        except Exception as e:
            logger.error(f"Installation error: {e}")
            self._update_status(f"✗ Error: {e}")
            messagebox.showerror("Error", str(e))

        finally:
            self._enable_buttons()

    def _on_custom_install_click(self) -> None:
        """Handle custom AI install button click."""
        user_input = self.custom_input.get().strip()
        if not user_input:
            messagebox.showwarning("No Input", "Please enter an installation request")
            return

        # Try to determine which app config to use
        apps = self.config_loader.load_applications()
        app_config = None

        for app_name, config in apps.get('applications', {}).items():
            if app_name.lower() in user_input.lower():
                app_config = config
                break

        if not app_config:
            messagebox.showwarning(
                "Unknown Application",
                "Could not determine application from request. Please use predefined installation."
            )
            return

        self._disable_buttons()
        self._update_status(f"Processing request: {user_input}")

        try:
            success = self.installer.install_with_ai(
                user_input,
                app_config,
                status_callback=self._update_status
            )

            if success:
                self._update_status("✓ Installation completed successfully!")
                messagebox.showinfo("Success", "Installation completed successfully!")
            else:
                self._update_status("✗ Installation failed")
                messagebox.showerror("Error", "Installation failed. Check logs for details.")

        except Exception as e:
            logger.error(f"AI installation error: {e}")
            self._update_status(f"✗ Error: {e}")
            messagebox.showerror("Error", str(e))

        finally:
            self._enable_buttons()

    def _on_open_click(self) -> None:
        """Handle open application button click."""
        app_name = self.open_input.get().strip()
        if not app_name:
            messagebox.showwarning("No Input", "Please enter an application name")
            return

        self._update_status(f"Searching for {app_name}...")

        try:
            import os
            search_path = "C:\\"
            found = False

            for root, dirs, files in os.walk(search_path):
                for file_name in files:
                    if app_name.lower() in file_name.lower() and file_name.endswith(".lnk"):
                        full_path = os.path.join(root, file_name)
                        self._update_status(f"Found: {full_path}")
                        os.startfile(full_path)
                        found = True
                        break
                if found:
                    break

            if found:
                self._update_status(f"✓ Opened {app_name}")
            else:
                self._update_status(f"✗ Could not find {app_name}")
                messagebox.showwarning("Not Found", f"Could not find {app_name}")

        except Exception as e:
            logger.error(f"Error opening application: {e}")
            self._update_status(f"✗ Error: {e}")
            messagebox.showerror("Error", str(e))

    def _disable_buttons(self) -> None:
        """Disable all action buttons."""
        self.install_button.config(state=tk.DISABLED)
        self.custom_button.config(state=tk.DISABLED)
        self.open_button.config(state=tk.DISABLED)

    def _enable_buttons(self) -> None:
        """Enable all action buttons."""
        self.install_button.config(state=tk.NORMAL)
        self.custom_button.config(state=tk.NORMAL)
        self.open_button.config(state=tk.NORMAL)

    def run(self) -> None:
        """Start the GUI application."""
        logger.info("Starting GUI application")
        self.root.mainloop()
