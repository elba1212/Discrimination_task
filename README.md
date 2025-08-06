# Face Discrimination Task - MATLAB Package

A MATLAB-based experimental paradigm for studying face discrimination abilities using morphed face stimuli. This package implements a 3-alternative forced choice (3AFC) discrimination task where participants view morphed faces and must identify which original face the morph most closely resembles.

## Overview

This package implements a novel face-morph discrimination task, designed by Ella Bar, to assess how participants generalize emotionally reinforced stimuli (from a separate reinforcement learning task). Participants are presented with blended (morphed) faces composed of three original identities and asked to judge which original face each morph most closely resembles. The experiment is built using Psychtoolbox, which handles stimulus presentation, participant input, and GUI dialogs. Participant responses are recorded and logged for later analysis.


### Key Features

- **3-Alternative Forced Choice Design**: Participants choose between three original faces
- **Morphed Stimuli**: Uses computer-generated morphs between original face stimuli
- **Training Module**: Optional training session to familiarize participants with the task
- **Response Time Measurement**: Records reaction times for each trial
- **Reward System**: Point-based feedback system
- **Multi-session Support**: Supports multiple experimental sessions with accumulated rewards
- **Hebrew Text Support**: Includes Hebrew text display with optional text flipping
- **MRI-Compatible**: Designed for use in MRI environments

## Requirements

### MATLAB Version
- MATLAB R2016b or later (recommended: R2019b+)

### Required Toolboxes
- **Psychtoolbox 3**: Essential for stimulus presentation and response collection
  - Download from: http://psychtoolbox.org/
  - Version 3.0.18 or later recommended

### System Requirements
- **Operating System**: Windows, macOS, or Linux
- **Display**: Monitor with 60Hz refresh rate or higher
- **Input**: Standard keyboard with arrow keys
- **Memory**: Minimum 4GB RAM (8GB+ recommended)
- **Storage**: At least 1GB free space for stimuli and data

### Additional Dependencies
- **Image Processing Toolbox** (MATLAB built-in)
- **Statistics and Machine Learning Toolbox** (MATLAB built-in)

## Installation

1. **Install MATLAB** (if not already installed)
2. **Install Psychtoolbox 3**:
   ```matlab
   % In MATLAB command window
   web('http://psychtoolbox.org/download.html')
   % Follow installation instructions for your platform
   ```
3. **Download this package** and extract to your desired location
4. **Set up stimuli**: Ensure the `stimuli_and_log` folder contains the required stimulus files

## File Structure

```
Discrimination_task/
├── mainMRI_DiscriminationTest3.m    # Main experiment script
├── facesDiscriminationTest3.m       # Core discrimination task function
├── TrainingDiscriminationTest3.m    # Training module
├── pathsLearningFaces.m             # Path configuration
├── save_to_log.m                    # Data logging utilities
├── save_to_log_trial.m              # Trial-level logging
├── test.m                           # Test script for setup verification
└── stimuli_and_log/
    ├── Stimuli/                     # Stimulus files (faces, instructions)
    ├── Log/                         # Output data directory
    └── Analysis/                    # Analysis scripts and results
```

## Usage

### Quick Start

1. **Navigate to the Discrimination_task directory** in MATLAB:
   ```matlab
   cd('path/to/Discrimination_task')
   ```

2. **Run the main experiment script**:
   ```matlab
   mainMRI_DiscriminationTest3
   ```

3. **Enter participant information** when prompted:
   - Subject number
   - Session number
   - Face gender (men/women)
   - Hebrew text flip setting
   - Training requirement

### Experiment Parameters

The experiment uses the following default parameters:
- **Number of original faces**: 3
- **Number of morphs**: 66 per face pair
- **Repetitions**: 6 per morph
- **Total trials**: 396 (66 morphs × 6 repetitions)
- **Response window**: 3 seconds
- **Stimulus duration**: 1.5 seconds
- **Reward magnitude**: 1 point per correct response

### Data Output

The experiment generates the following data files:
- `discriminationTest_[subject]_session_[session].mat`: Main experimental data
- `accumWinnings_[subject].mat`: Accumulated reward data

### Data Structure

The output log contains:
- **RT**: Response times for each trial
- **correct**: Accuracy (1=correct, -1=incorrect, 0=ambiguous)
- **Response**: Key press responses (1=left, 2=down, 3=right)
- **subjectChoice**: Face choice with respect to original stimuli
- **shuffledTrialsOrder**: Trial presentation order
- **ExpTime**: Total experiment duration
- **faces**: Original face stimuli used
- **Training data**: Separate fields for training session data

## Configuration

### Paths Setup
Edit `pathsLearningFaces.m` to configure file paths:
- Stimulus directories for men's and women's faces
- Log output directory
- Text instruction files
- Training stimuli

### Experiment Parameters
Modify parameters in `mainMRI_DiscriminationTest3.m`:
- Number of morphs (`nMorphs`)
- Number of repetitions (`Repetitions`)
- Reward magnitude (`RewardMagnitude`)
- Morph division assignments (`morphs_division`)

## Troubleshooting

### Common Issues

1. **Psychtoolbox not found**:
   - Ensure Psychtoolbox is properly installed
   - Run `PsychtoolboxVersion` to verify installation

2. **Display issues**:
   - Check monitor refresh rate settings
   - Verify Psychtoolbox display configuration

3. **Hebrew text display problems**:
   - Use the text flip option (`flipText = 'y'`)
   - Ensure proper font support

4. **Stimulus loading errors**:
   - Verify stimulus file paths in `pathsLearningFaces.m`
   - Check that all required image files exist

### Testing Setup
Run the test script to verify your setup:
```matlab
test
```

## Citation

If you use this package in your research, please cite:

```
Bar, E., et al. (Year). Face Discrimination Task - MATLAB Package. 
[Software]. Available: [URL]
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

If you wish to use this task in you project please write to Ellapaltiel@gmail.com.

