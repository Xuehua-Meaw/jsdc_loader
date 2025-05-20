@echo off
REM Build and push Python package to PyPI

REM Load environment variables from .env file if it exists
if exist ".env" (
    echo loading environment variables
    for /F "tokens=*" %%A in (.env) do set %%A
)

REM Clean previous builds
if exist "dist" rd /s /q "dist"
if exist "build" rd /s /q "build"
if exist "*.egg-info" rd /s /q "*.egg-info"

REM Build package
python -m build

REM Upload package to PyPI using token authentication
if defined PYPI_TOKEN (
    echo use token to upload package
    python -m twine upload dist/* --non-interactive --username __token__ --password %PYPI_TOKEN%
) else (
    echo PYPI_TOKEN environment variable is not set, use interactive authentication
    python -m twine upload dist/*
)