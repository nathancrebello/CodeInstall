# Installer Automation Tool

An intelligent automation tool that streamlines software installation using computer vision and AI assistance. Built with Python, this tool automatically navigates installation wizards, clicks buttons, and configures software without manual intervention.

## Features

- **Automated Installation**: Uses computer vision (OCR) to detect and click UI elements during installation
- **AI-Powered Downloads**: Leverages OpenAI to generate download scripts for software
- **Multi-Application Support**: Pre-configured for Python, PyCharm, Java, IntelliJ IDEA, and Node.js
- **User-Friendly GUI**: Clean Tkinter interface for easy operation
- **Extensible**: Easy to add new applications via YAML configuration
- **Robust Error Handling**: Comprehensive logging and error recovery
- **Modular Architecture**: Clean separation of concerns for maintainability

## Architecture

```
installer_automation/
├── src/
│   ├── core/              # Core automation logic
│   │   ├── installer.py        # Main installer orchestration
│   │   ├── screen_automation.py # Computer vision & GUI automation
│   │   └── ai_assistant.py     # OpenAI integration
│   ├── gui/               # User interface
│   │   └── application.py      # Tkinter GUI application
│   ├── utils/             # Utility modules
│   │   ├── admin.py           # Admin privilege management
│   │   ├── logger.py          # Logging configuration
│   │   └── config_loader.py   # Configuration management
│   └── main.py           # Application entry point
├── config/               # Configuration files
│   ├── settings.yaml          # General settings
│   └── applications.yaml      # Application definitions
├── assets/              # UI element images for matching
│   └── ui_elements/
└── logs/                # Application logs
```

## Prerequisites

- **Operating System**: Windows (required for admin automation)
- **Python**: 3.8 or higher
- **Tesseract OCR**: Must be installed separately
  - Download from: https://github.com/UB-Mannheim/tesseract/wiki
  - Default path: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- **OpenAI API Key** (optional): Required for AI-powered installation features

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd CodeInstall
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR**:
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install to default location or update path in `config/settings.yaml`

4. **Configure the application**:
   - Copy `.env.example` to `.env`:
     ```bash
     copy .env.example .env
     ```
   - Edit `.env` and add your OpenAI API key (if using AI features):
     ```
     OPENAI_API_KEY=your_key_here
     ```
   - Review and update `config/settings.yaml` as needed
   - Update Tesseract path in `config/settings.yaml` if installed elsewhere

5. **Prepare UI element images**:
   - Add installation wizard button images to `assets/ui_elements/`
   - Organize by application (e.g., `assets/ui_elements/Python/`, etc.)
   - Images should be screenshots of buttons like "Next", "Install", "Finish"

## Usage

### Running the Application

```bash
python src/main.py
```

The application will request administrator privileges (required for some installations).

### Using the GUI

1. **Standard Installation**:
   - Select an application from the dropdown
   - Click "Install" button
   - The tool will download and automatically install the software

2. **AI-Assisted Installation**:
   - Enter a custom request (e.g., "Download Python 3.11")
   - Click "Install with AI"
   - The AI will generate a download script and automate installation

3. **Opening Installed Applications**:
   - Enter the application name
   - Click "Open"
   - The tool will search for and launch the application

### Adding New Applications

Edit `config/applications.yaml`:

```yaml
my_application:
  display_name: "My Application"
  window_title_match: "MyApp"
  download_url: "https://example.com/installer.exe"
  installer_extension: "exe"
  ui_elements_folder: "MyApp"
  post_install_prompt: null
  suggested_ide: null
```

Then add UI element images to `assets/ui_elements/MyApp/`.

## Configuration

### Settings (`config/settings.yaml`)

- **OpenAI**: API key and model configuration
- **Paths**: Tesseract, downloads, UI elements, logs
- **Automation**: Timeouts, retries, delays
- **Logging**: Log levels and output
- **GUI**: Window dimensions and theme

### Applications (`config/applications.yaml`)

Define supported applications with:
- Download URLs
- Window title patterns for detection
- UI element image folders
- Post-installation prompts

## How It Works

1. **Download Phase**:
   - Downloads installer from configured URL or uses AI to generate download script
   - Saves to Downloads folder

2. **Launch Phase**:
   - Executes the installer
   - Waits for installer window to appear

3. **Automation Phase**:
   - Continuously scans screen for UI element images
   - Clicks buttons in order (Next → Accept → Install → Finish)
   - Monitors for changes to determine completion

4. **Completion**:
   - Detects when no more clicks are needed
   - Optionally prompts for related software (e.g., IDE after language)

## Technical Highlights

- **Computer Vision**: Uses PyAutoGUI and Tesseract OCR for UI element detection
- **Window Management**: PyWinAuto for window manipulation
- **AI Integration**: OpenAI API for intelligent script generation
- **Robust Logging**: Comprehensive logs for debugging and monitoring
- **Configuration-Driven**: Easy customization without code changes
- **Error Recovery**: Graceful handling of failures with retry logic

## Security Notes

- Requires administrator privileges for system-wide installations
- **Never commit API keys** to version control
- Use environment variables for sensitive data
- Review AI-generated code before execution (in production scenarios)

## Limitations

- **Windows Only**: Uses Windows-specific APIs (pywinauto, ctypes)
- **UI Changes**: Installation wizards with different layouts may need new image captures
- **Internet Required**: For downloading installers and AI features
- **Screen Resolution**: UI element matching may be affected by different resolutions

## Future Enhancements

- Cross-platform support (macOS, Linux)
- Machine learning for adaptive UI element detection
- Installer database with community contributions
- Silent installation support (command-line parameters)
- Installation history and rollback capability

## Troubleshooting

**"Tesseract not found"**:
- Ensure Tesseract is installed
- Update path in `config/settings.yaml`
- Set `TESSERACT_PATH` environment variable

**"Image not found on screen"**:
- Capture new screenshots of installer buttons
- Save to appropriate folder in `assets/ui_elements/`
- Ensure screen resolution matches captured images

**"AI features not working"**:
- Verify OpenAI API key is set in `.env`
- Check internet connection
- Review logs for API errors

## Contributing

This project demonstrates:
- Clean architecture and modular design
- Configuration management best practices
- Error handling and logging
- Integration of multiple technologies
- Documentation and code quality

## License

This project is provided as a portfolio demonstration. Feel free to use as reference.

## Contact

For questions or feedback about this project, please reach out through my portfolio or LinkedIn.

---

**Note**: This tool is designed for educational and automation purposes. Always review software licenses and terms of service before automated installation.
