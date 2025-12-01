# Migration Guide

This guide helps you migrate from the old code structure to the new refactored version.

## What's Changed

### Old Structure
- All code in single files (main.py, second_main.py, third_main.py)
- Hardcoded paths and API keys
- No separation of concerns
- Duplicated code

### New Structure
- Modular architecture with separate concerns
- Configuration files for settings
- Reusable components
- Professional code organization
- Comprehensive documentation

## Migration Steps

### 1. Move Your UI Element Images

The old code referenced images from:
```
C:\Users\natha\OneDrive\Documents\CodeInstall\Images\
```

New location:
```
assets/ui_elements/
```

**Action**: Copy your existing images:
```bash
# Example: Copy Python images
xcopy "C:\Users\natha\OneDrive\Documents\CodeInstall\Images\Python" "assets\ui_elements\Python" /E /I

# Example: Copy PyCharm images
xcopy "C:\Users\natha\OneDrive\Documents\CodeInstall\Images\PyCharm" "assets\ui_elements\PyCharm" /E /I
```

Do this for all application folders:
- Python
- PyCharm
- Java
- IntelliJ
- Node
- pcsetup (if used)

### 2. Configure Tesseract Path

Old code had hardcoded path:
```python
tess.pytesseract.tesseract_cmd = r'C:\Users\natha\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
```

New approach - Update `config/settings.yaml`:
```yaml
paths:
  tesseract_executable: "C:\\Users\\natha\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"
```

Or set environment variable:
```bash
set TESSERACT_PATH=C:\Users\natha\AppData\Local\Programs\Tesseract-OCR\tesseract.exe
```

### 3. Setup OpenAI API Key

Old code had exposed API key:
```python
client = OpenAI(api_key="OPEN_API_KEY")
```

**NEVER commit your real API key!**

New approach - Create `.env` file:
```bash
copy .env.example .env
```

Edit `.env`:
```
OPENAI_API_KEY=your_actual_api_key_here
```

### 4. Update Download Links

Old code had download links in `Links/Download_Links.txt`.

New location: `config/applications.yaml`

Review and update URLs in the applications section.

### 5. Test the New Version

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure settings:
   - Update `config/settings.yaml`
   - Update `config/applications.yaml`
   - Create `.env` with your API key

3. Run the application:
   ```bash
   python src/main.py
   ```

## Key Differences

### Configuration
- **Old**: Hardcoded paths throughout code
- **New**: Centralized in `config/settings.yaml`

### Application Definitions
- **Old**: Scattered if/else statements
- **New**: Structured YAML in `config/applications.yaml`

### Error Handling
- **Old**: Minimal, try/except with prints
- **New**: Comprehensive logging system

### Code Organization
- **Old**: Single large file with mixed concerns
- **New**: Modular structure with clear responsibilities

### Security
- **Old**: API keys in code (security risk!)
- **New**: Environment variables, never committed

## Benefits of New Version

1. **Maintainability**: Easy to understand and modify
2. **Extensibility**: Add new apps by editing YAML
3. **Security**: No hardcoded credentials
4. **Portability**: Configuration separate from code
5. **Professional**: Follows Python best practices
6. **Debuggability**: Comprehensive logging
7. **Testability**: Modular design enables unit testing
8. **Recruiter-Ready**: Clean code demonstrates skill

## Keeping Old Code

The old files (main.py, second_main.py, etc.) are ignored by git but kept for reference. You can:
- Keep them for comparison
- Delete them once migration is complete
- Reference them if you need to understand old logic

## Need Help?

If you encounter issues during migration:
1. Check logs in `logs/installer_automation.log`
2. Review configuration files for typos
3. Ensure all paths are correct for your system
4. Verify Tesseract is installed correctly
5. Confirm API key is valid (if using AI features)

## Next Steps

After successful migration:
1. Test all applications you frequently use
2. Update download URLs if needed
3. Capture new UI element images if installations have changed
4. Customize GUI theme in settings
5. Add any custom applications to `config/applications.yaml`

---

**Remember**: The new version is designed to be shown to recruiters. Keep your API keys safe and never commit them to version control!
