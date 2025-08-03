# Face Discrimination Experiment

A Python package for conducting face discrimination psychological experiments, converted from MATLAB PsychToolbox implementation.

## Overview

This package provides a complete framework for running face discrimination experiments where participants:
1. View a morphed face stimulus
2. Choose which of several original faces is most similar to the morph
3. Receive feedback and points based on their choices

The package includes training sessions, configurable experiment parameters, comprehensive logging, and data analysis capabilities.

## Features

- **Complete Experiment Framework**: Training, main experiment, and results display
- **Flexible Configuration**: Customizable parameters for different experimental needs
- **Comprehensive Logging**: JSON and CSV output with detailed trial-by-trial data
- **Multi-session Support**: Handles multiple sessions with accumulated scores
- **Hebrew Text Support**: Includes original Hebrew instructions with flip support
- **Error Handling**: Robust error tracking and recovery
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

### Requirements

- Python 3.8 or higher
- PsychoPy 2023.1.0 or higher
- NumPy, SciPy, Pandas, Matplotlib, Pillow, OpenCV

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Package

```bash
pip install -e .
```

## Quick Start

### Basic Usage

```python
from faces_discrimination import run_experiment

# Run with dialog configuration
results = run_experiment()
```

### Custom Configuration

```python
from faces_discrimination import run_experiment, ExperimentConfig

# Create custom configuration
config = ExperimentConfig(
    subject_number=101,
    session=1,
    gender_faces="m",  # "m" for men, "w" for women
    include_training=True,
    repetitions=6,
    n_morphs=66
)

# Run experiment
results = run_experiment(config=config)
```

### Command Line Usage

```bash
# Run the experiment
python -m faces_discrimination.main

# Or use the console script (after installation)
faces-discrimination
```

## Directory Structure

```
faces_discrimination/
├── __init__.py           # Package initialization
├── main.py              # Main experiment runner
├── config.py            # Configuration management
├── discrimination_test.py # Main experiment logic
├── training.py          # Training session logic
├── utils.py             # Utilities (paths, logging)
└── test_simple.py       # Basic functionality tests

stimuli_and_log/         # Expected data directory structure
├── Stimuli/
│   ├── morphs_ella/
│   │   ├── morphs men/11/
│   │   ├── morphs women/11/
│   │   └── training/
│   ├── pairs/
│   └── text/
└── Log/                 # Output logs directory
```

## Configuration

The `ExperimentConfig` class provides comprehensive control over experiment parameters:

### Subject and Session Parameters
- `subject_number`: Participant ID
- `session`: Session number (1, 2, 3...)
- `gender_faces`: Face gender ("m" or "w")
- `flip_hebrew_text`: Flip Hebrew text for display issues
- `include_training`: Whether to include training session

### Experiment Parameters
- `n_faces`: Number of original faces (default: 3)
- `n_morphs`: Number of morphs on the axis (default: 66)
- `repetitions`: Number of repetitions per morph (default: 6)
- `training_trials`: Number of training trials (default: 6)

### Timing Parameters
- `morph_display_time`: How long to show morphs (default: 1.5s)
- `response_timeout`: Response timeout (default: 3.0s)
- `feedback_display_time`: Feedback duration (default: 0.2s)

### Display Parameters
- `background_color`: Screen background color
- `text_color`: Text color
- `text_size`: Font size
- `screen_number`: Display screen number

## Data Output

### Log Files

The experiment generates several output files in `stimuli_and_log/Log/{subject_number}/`:

1. **Main log file**: `discriminationTest_{subject}_{session}.json`
   - Complete experiment data in JSON format
   - Trial-by-trial responses, reaction times, correctness
   - Configuration parameters
   - Error events and summary statistics

2. **CSV file**: `discriminationTest_{subject}_{session}.csv`
   - Trial data in spreadsheet format for easy analysis

3. **Accumulated winnings**: `accumWinnings_{subject}.json`
   - Cross-session accumulated points

### Data Structure

```python
{
    "config": {...},           # Experiment configuration
    "start_time": float,       # Experiment start time
    "faces": [1, 2, 3],       # Original face numbers used
    "trials": [               # Trial-by-trial data
        {
            "trial_index": 0,
            "morph_number": 15,
            "response": 2,
            "subject_choice": 2,
            "correct": 1,
            "rt": 0.856,
            "key_pressed": "down"
        }, ...
    ],
    "training_trials": [...], # Training trial data
    "errors": {              # Error events
        "wrong_key_trials": [...],
        "too_slow_trials": [...]
    },
    "summary": {             # Summary statistics
        "total_trials": 396,
        "mean_rt": 0.834,
        "accuracy": 0.73,
        "cumulative_reward": 287
    }
}
```

## API Reference

### Main Functions

#### `run_experiment(config=None, base_path=None)`
Run the complete face discrimination experiment.

**Parameters:**
- `config` (ExperimentConfig, optional): Experiment configuration
- `base_path` (str, optional): Base path for data files

**Returns:**
- `dict`: Experiment results with status, summary, and log data

### Classes

#### `ExperimentConfig`
Configuration class for experiment parameters.

**Key Methods:**
- `from_dialog()`: Create config from user dialog
- `validate()`: Validate configuration parameters
- `get_hebrew_text(key)`: Get Hebrew text with proper formatting

#### `FacesDiscriminationTest`
Main experiment class.

**Key Methods:**
- `run()`: Execute complete experiment
- `setup_experiment()`: Initialize experiment parameters
- `run_training()`: Execute training session
- `run_experiment_trials()`: Execute main trials

#### `PathManager`
File path management utility.

**Key Methods:**
- `get_morph_path(gender, morph_number)`: Get path to morph image
- `get_original_path(gender, original_number)`: Get path to original face
- `get_log_file_path(subject, session)`: Get path for log file

#### `Logger`
Experiment logging utility.

**Key Methods:**
- `log_trial(trial_data)`: Log single trial data
- `save_log(subject, session)`: Save experiment data
- `load_log(path_manager, subject, session)`: Load existing data

## Examples

See the `examples/` directory for detailed usage examples:

- `basic_usage.py`: Basic experiment execution and data analysis
- More examples coming soon...

## Testing

Run basic functionality tests:

```python
from faces_discrimination.test_simple import run_all_tests
run_all_tests()
```

Or from command line:
```bash
python -m faces_discrimination.test_simple
```

## Migration from MATLAB

This package directly converts the following MATLAB files:

| MATLAB File | Python Module | Description |
|-------------|---------------|-------------|
| `mainMRI_DiscriminationTest3.m` | `main.py` | Main experiment runner |
| `facesDiscriminationTest3.m` | `discrimination_test.py` | Core experiment logic |
| `TrainingDiscriminationTest3.m` | `training.py` | Training session |
| `pathsLearningFaces.m` | `utils.py` (PathManager) | Path management |
| `save_to_log.m` | `utils.py` (Logger) | Data logging |
| `test.m` | `test_simple.py` | Basic functionality tests |

### Key Differences

1. **Configuration**: MATLAB's `inputdlg` replaced with PsychoPy GUI dialogs
2. **Display**: PsychToolbox Screen functions replaced with PsychoPy visual stimuli
3. **Data Format**: MAT files replaced with JSON/CSV for better cross-platform compatibility
4. **Error Handling**: More robust error handling and recovery
5. **Modularity**: Better separation of concerns with dedicated classes

## Troubleshooting

### Common Issues

1. **PsychoPy Installation**: Ensure PsychoPy is properly installed with all dependencies
2. **Display Issues**: Check screen number configuration if using multiple displays
3. **File Paths**: Ensure the `stimuli_and_log` directory structure exists
4. **Hebrew Text**: Use `flip_hebrew_text=True` if Hebrew text appears backwards

### Debug Mode

For debugging, you can run with reduced parameters:

```python
config = ExperimentConfig(
    n_morphs=5,        # Fewer morphs
    repetitions=1,     # Single repetition
    include_training=False,  # Skip training
    response_timeout=10.0    # Longer timeout
)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this software in your research, please cite:

```
Face Discrimination Experiment Package (2024)
Converted from MATLAB PsychToolbox implementation
https://github.com/your-repo/faces-discrimination-experiment
```

## Support

For questions or issues:
1. Check the troubleshooting section above
2. Review the examples in the `examples/` directory
3. Open an issue on the GitHub repository
4. Contact the maintainers

## Acknowledgments

- Original MATLAB implementation contributors
- PsychoPy development team
- Research participants and collaborators