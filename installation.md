# Lost and Found - Installation Guide

This guide provides step-by-step instructions on how to install Python and Django for Lost and Found webapp.

## System Requirements

Before installing Python and Django, ensure that your system meets the following requirements:

### For Python 3.10

- **Operating System:** Compatible with Windows, macOS, or Linux distributions.
- **Disk Space:** Approximately 200 MB for Python installation.
- **Memory (RAM):** At least 1 GB for smooth operation.

### For Django 4.2

- **Python:** Compatible with Python 3.10 (as specified in this guide).
- **Operating System:** Compatible with Windows, macOS, or Linux distributions.
- **Disk Space:** Additional space required for Django and project files.
- **Memory (RAM):** At least 2 GB is recommended for Django projects.


## Python Installation

### Installing Python 3.10

1. **Windows:**
   - Visit the [Python downloads page](https://www.python.org/downloads/release/python-310/) and download the installer for Windows.
   - Run the installer, check the box "Add Python 3.10 to PATH," and follow the installation prompts.

2. **macOS:**
   - Open a terminal window and install Homebrew if you haven't already:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Install Python 3.10 using Homebrew:
     ```bash
     brew install python@3.10
     ```

3. **Linux:**
   - Use the package manager specific to your distribution to install Python 3.10. For example:
     - Ubuntu/Debian:
       ```bash
       sudo apt update
       sudo apt install python3.10
       ```
     - CentOS/Fedora:
       ```bash
       sudo dnf install python3.10
       ```

### Installing Python Versions Below 3.10

For versions below 3.10, you can use various methods:

- For Windows and macOS, visit the [Python downloads page](https://www.python.org/downloads/) and choose the desired version from the list of releases.
- On Linux, use your package manager or compile from source if the desired version is not available in the repositories.

### Verifying Installation

Once the installation is complete, verify the Python version:

- Open a terminal or command prompt.
- Type `python --version` or `python3 --version` and press Enter.
- The output should display the installed Python version.

## Installing Django 4.2

After installing Python, follow these steps to install Django 4.2 using pip (Python's package manager):

1. Open a terminal or command prompt.

2. Install Django 4.2 using pip:
   ```bash
   pip install Django==4.2

### Verifying Installation

Once the installation is complete, verify the Django version:

- Open a terminal or command prompt.
- Type `python -m django --version` or `python3 -m django --version` and press Enter.
- The output should display the installed Django version.

## Additional Package Installation

### Installation of Django Crispy Forms


After installing Django, follow these steps to install django-crispy-forms using pip:

1. Open a terminal or command prompt.

2. Install django-crispy-forms using pip:
   ```bash
   pip install django-crispy-forms

Once installed, add 'crispy_forms' to your Django project's INSTALLED_APPS in the settings.py file:

#### Add 'crispy_forms' to settings.py

```bash
INSTALLED_APPS = [
    # Other installed apps...
    'crispy_forms',
]
```
#### Configure crispy-forms in your settings.py

```bash
CRISPY_TEMPLATE_PACK = 'bootstrap5'  # Use 'bootstrap5' or another supported template pack
```

### Installing crispy-bootstrap5

After installing Django and django-crispy-forms, follow these steps to install crispy-bootstrap5:

1. **Install `django-crispy-forms` (if not installed already):**
   ```bash
   pip install django-crispy-forms

2. **Install `crispy-bootstrap5`:**
   ```bash
   pip install crispy-bootstrap5

3. **Configure crispy-bootstrap5 in your Django project:**
   ```bash
   # settings.py

CRISPY_ALLOWED_TEMPLATE_PACKS = (
    'bootstrap5',  # Add 'bootstrap5' to use Bootstrap 5
)
   ```

Now, you're ready to proceed with setting up and running your project!
