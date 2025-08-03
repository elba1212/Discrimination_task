# Changelog

All notable changes to the Face Discrimination Experiment package will be documented in this file.

## [1.0.0] - 2024-12-19

### Added
- Initial release of Python package converted from MATLAB
- Complete face discrimination experiment framework
- PsychoPy-based visual presentation system
- Comprehensive configuration management system
- JSON/CSV data logging with full trial-by-trial data
- Multi-session support with accumulated winnings tracking
- Training session with customizable parameters
- Hebrew text support with flip option for display compatibility
- Robust error handling and recovery mechanisms
- Cross-platform compatibility (Windows, macOS, Linux)
- Command-line interface and programmatic API
- Comprehensive documentation and examples
- Basic functionality testing suite

### Converted from MATLAB
- `mainMRI_DiscriminationTest3.m` → `main.py`
  - Main experiment runner with dialog-based configuration
  - Session management and file existence checking
  - Multi-session accumulated winnings handling
  
- `facesDiscriminationTest3.m` → `discrimination_test.py`
  - Core experiment logic with trial presentation
  - Response collection and accuracy calculation
  - Stimulus positioning and display management
  - Results presentation with winnings display
  
- `TrainingDiscriminationTest3.m` → `training.py`
  - Training session implementation
  - Repeatable training with user choice
  - Training-specific stimulus management
  
- `pathsLearningFaces.m` → `utils.py` (PathManager)
  - File path management for stimuli and logs
  - Automatic directory creation
  - Cross-platform path handling
  
- `save_to_log.m` → `utils.py` (Logger)
  - Comprehensive data logging in JSON format
  - Additional CSV export for analysis
  - Summary statistics calculation
  
- `test.m` → `test_simple.py`
  - Basic PsychoPy functionality testing
  - Fixation cross display test
  - Text and image rendering tests

### Key Improvements Over MATLAB Version

#### Technology Stack
- **PsychoPy instead of PsychToolbox**: More modern, Python-native, cross-platform
- **JSON/CSV instead of MAT files**: Better data portability and analysis compatibility
- **Object-oriented design**: Better code organization and maintainability
- **Modern Python features**: Type hints, dataclasses, pathlib

#### Enhanced Functionality
- **Configuration Management**: Centralized, validated configuration system
- **Error Handling**: Comprehensive error tracking and graceful recovery
- **Logging**: Enhanced logging with timestamps and metadata
- **Data Analysis**: Built-in summary statistics and analysis tools
- **Testing**: Automated functionality testing
- **Documentation**: Comprehensive API documentation and examples

#### User Experience
- **GUI Dialogs**: Improved user input dialogs with PsychoPy
- **Command Line**: Console script entry point for easy execution
- **Progress Tracking**: Better feedback during experiment execution
- **Cross-session**: Improved session management and data continuity

#### Developer Experience
- **Modularity**: Clean separation of concerns with dedicated classes
- **Extensibility**: Easy to modify and extend for new experiments
- **Package Management**: Standard Python packaging with setup.py
- **Dependencies**: Clear dependency management with requirements.txt

### Technical Details

#### Dependencies
- Python 3.8+
- PsychoPy 2023.1.0+
- NumPy 1.21.0+
- SciPy 1.7.0+
- Matplotlib 3.5.0+
- Pandas 1.3.0+
- Pillow 8.3.0+
- OpenCV 4.5.0+

#### File Format Changes
- **Configuration**: Python dataclass → JSON serializable
- **Logs**: MATLAB struct → JSON with nested structure
- **Analysis Data**: MAT files → CSV for spreadsheet compatibility
- **Timing**: MATLAB datenum → ISO 8601 timestamps

#### Display System Changes
- **Window Management**: Screen() → visual.Window()
- **Text Rendering**: DrawFormattedText → visual.TextStim
- **Image Display**: PutImage/DrawTexture → visual.ImageStim
- **Geometry**: Custom coordinates → PsychoPy coordinate system
- **Timing**: GetSecs/WaitSecs → core.getTime()/core.wait()

#### Input System Changes
- **Keyboard**: KbWait/KbCheck → event.waitKeys()
- **Response Collection**: PsychHID → event system
- **Key Mapping**: Keycode numbers → string names
- **Timing**: Hardware timestamps → software timestamps

#### Data Structure Changes
```
MATLAB struct fields → Python dict keys:
- RT → rt
- Response → response  
- correct → correct
- subjectChoice → subject_choice
- wrongKeyTrial → wrong_key_trials
- TooSlowTrial → too_slow_trials
- ExpTime → experiment_time
```

### Migration Guide

#### For Researchers
1. **Data Format**: Existing MAT files need conversion to JSON/CSV
2. **Analysis Scripts**: Update to use JSON/CSV instead of MAT files
3. **Configuration**: Use ExperimentConfig instead of inputdlg
4. **Results**: Same core data structure with improved metadata

#### For Developers
1. **API Changes**: Function-based → class-based architecture
2. **Error Handling**: Use try/catch → try/except with specific handling
3. **Path Management**: Manual paths → PathManager class
4. **Configuration**: Global variables → ExperimentConfig object

### Backward Compatibility

#### Data Compatibility
- Core experimental data remains compatible
- Trial structure preserved with additional metadata
- Timing precision maintained
- Response mapping identical

#### Workflow Compatibility
- Same experimental procedure and timing
- Identical stimulus presentation logic
- Same response collection methods
- Compatible results and analysis

### Known Issues
- Hebrew text rendering may vary across platforms
- Fullscreen mode behavior differs from MATLAB version
- Some timing precision differences due to Python vs MATLAB

### Future Plans
- [ ] Data conversion utilities for existing MATLAB data
- [ ] Additional analysis and visualization tools
- [ ] Advanced configuration validation
- [ ] Performance optimization
- [ ] Extended documentation and tutorials
- [ ] Integration with common analysis pipelines