from setuptools import setup, find_packages

setup(
    name="faces-discrimination-experiment",
    version="1.0.0",
    description="Python package for face discrimination psychological experiments (converted from MATLAB)",
    author="Converted from MATLAB",
    packages=find_packages(),
    install_requires=[
        "psychopy>=2023.1.0",
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.5.0",
        "pandas>=1.3.0",
        "pillow>=8.3.0",
        "opencv-python>=4.5.0",
        "tk>=0.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
        ]
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Psychology",
    ],
    entry_points={
        "console_scripts": [
            "faces-discrimination=faces_discrimination.main:main",
        ],
    },
)