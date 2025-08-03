#!/usr/bin/env python3
"""
Installation helper script for the faces discrimination experiment package.
"""
import subprocess
import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is adequate."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python version {sys.version.split()[0]} is adequate")
    return True


def install_dependencies():
    """Install package dependencies."""
    print("Installing dependencies...")
    
    try:
        # Install from requirements.txt
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✓ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False


def install_package():
    """Install the package in development mode."""
    print("Installing package in development mode...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-e", "."
        ])
        print("✓ Package installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing package: {e}")
        return False


def create_directories():
    """Create necessary directories for the experiment."""
    print("Creating experiment directories...")
    
    directories = [
        "stimuli_and_log/Stimuli/morphs_ella/morphs men/11",
        "stimuli_and_log/Stimuli/morphs_ella/morphs women/11", 
        "stimuli_and_log/Stimuli/morphs_ella/training",
        "stimuli_and_log/Stimuli/pairs",
        "stimuli_and_log/Stimuli/text",
        "stimuli_and_log/Log",
        "stimuli_and_log/Analysis"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  Created: {directory}")
    
    print("✓ Experiment directories created")
    return True


def test_installation():
    """Test the installation by importing the package."""
    print("Testing installation...")
    
    try:
        import faces_discrimination
        print(f"✓ Package imported successfully (version {faces_discrimination.__version__})")
        
        # Test basic functionality
        from faces_discrimination.test_simple import run_text_test
        success = run_text_test()
        
        if success:
            print("✓ Basic functionality test passed")
        else:
            print("⚠ Basic functionality test failed (but package is installed)")
            
        return True
        
    except ImportError as e:
        print(f"✗ Error importing package: {e}")
        return False


def main():
    """Main installation process."""
    print("Face Discrimination Experiment Package - Installation")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\nInstallation failed at dependency installation step.")
        sys.exit(1)
    
    # Install package
    if not install_package():
        print("\nInstallation failed at package installation step.")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("\nWarning: Could not create all directories.")
    
    # Test installation
    if not test_installation():
        print("\nWarning: Installation test failed.")
    
    print("\n" + "=" * 60)
    print("Installation completed!")
    print("\nNext steps:")
    print("1. Place your stimulus images in the stimuli_and_log/Stimuli/ directories")
    print("2. Run the experiment with: python -m faces_discrimination.main")
    print("3. Or run: faces-discrimination")
    print("4. Check examples/ directory for usage examples")
    
    print("\nFor help, see README.md or run:")
    print("  python -m faces_discrimination.test_simple")


if __name__ == "__main__":
    main()