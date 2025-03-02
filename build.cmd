@echo off
REM Build and push Python package to PyPI

REM Clean previous builds
if exist "dist" rd /s /q "dist"
if exist "build" rd /s /q "build"
if exist "*.egg-info" rd /s /q "*.egg-info"

REM Build package
python -m build