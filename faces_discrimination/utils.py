"""
Utility functions for face discrimination experiments.
"""
import os
import json
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from dataclasses import asdict

from .config import ExperimentConfig


class PathManager:
    """Manages file paths for the experiment, similar to pathsLearningFaces.m"""
    
    def __init__(self, base_path: Optional[Union[str, Path]] = None):
        """
        Initialize path manager.
        
        Args:
            base_path: Base directory for the experiment. If None, uses current directory.
        """
        if base_path is None:
            self.base_path = Path.cwd()
        else:
            self.base_path = Path(base_path)
            
        # Create main directories
        self.stimuli_path = self.base_path / "stimuli_and_log" / "Stimuli"
        self.log_path = self.base_path / "stimuli_and_log" / "Log"
        self.analysis_path = self.base_path / "stimuli_and_log" / "Analysis"
        
        # Specific stimuli paths
        self.faces_path_men = self.stimuli_path / "morphs_ella" / "morphs men" / "11"
        self.faces_path_women = self.stimuli_path / "morphs_ella" / "morphs women" / "11"
        self.pairs_path = self.stimuli_path / "pairs"
        self.text_path = self.stimuli_path / "text"
        self.training_path = self.stimuli_path / "morphs_ella" / "training"
        
        # Create directories if they don't exist
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create directories if they don't exist."""
        for path in [self.log_path, self.analysis_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    def get_faces_path(self, gender: str) -> Path:
        """Get the path for face stimuli based on gender."""
        if gender.lower() == 'm':
            return self.faces_path_men
        elif gender.lower() == 'w':
            return self.faces_path_women
        else:
            raise ValueError("Gender must be 'm' or 'w'")
    
    def get_morph_path(self, gender: str, morph_number: int) -> Path:
        """Get the full path to a specific morph image."""
        faces_path = self.get_faces_path(gender)
        return faces_path / f"{morph_number}.jpg"
    
    def get_original_path(self, gender: str, original_number: int) -> Path:
        """Get the full path to an original face image."""
        faces_path = self.get_faces_path(gender)
        return faces_path / "originals" / f"{original_number}.jpg"
    
    def get_instruction_path(self, instruction_name: str) -> Path:
        """Get the full path to an instruction image."""
        return self.text_path / f"{instruction_name}.jpg"
    
    def get_training_morph_path(self, morph_number: int) -> Path:
        """Get the full path to a training morph image."""
        return self.training_path / f"{morph_number}.jpg"
    
    def get_subject_log_dir(self, subject_number: int) -> Path:
        """Get the log directory for a specific subject."""
        subject_dir = self.log_path / str(subject_number)
        subject_dir.mkdir(exist_ok=True)
        return subject_dir
    
    def get_log_file_path(self, subject_number: int, session: int, experiment_type: str = "discriminationTest") -> Path:
        """Get the full path for a log file."""
        subject_dir = self.get_subject_log_dir(subject_number)
        return subject_dir / f"{experiment_type}_{subject_number}_session_{session}.json"
    
    def get_accumulated_winnings_path(self, subject_number: int) -> Path:
        """Get the path for accumulated winnings file."""
        subject_dir = self.get_subject_log_dir(subject_number)
        return subject_dir / f"accumWinnings_{subject_number}.json"


class Logger:
    """Handles experiment logging, similar to save_to_log.m functionality"""
    
    def __init__(self, path_manager: PathManager, config: ExperimentConfig):
        """
        Initialize logger.
        
        Args:
            path_manager: PathManager instance
            config: ExperimentConfig instance
        """
        self.path_manager = path_manager
        self.config = config
        self.log_data = {}
        
    def initialize_log(self, start_time: float, faces: List[int]):
        """Initialize the log structure."""
        self.log_data = {
            "config": asdict(self.config),
            "start_time": start_time,
            "faces": faces,
            "trials": [],
            "training_trials": [],
            "errors": {
                "wrong_key_trials": [],
                "too_slow_trials": []
            },
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "version": "1.0.0"
            }
        }
    
    def log_trial(self, trial_data: Dict[str, Any]):
        """Log data for a single trial."""
        trial_data["timestamp"] = datetime.now().isoformat()
        self.log_data["trials"].append(trial_data)
    
    def log_training_trial(self, trial_data: Dict[str, Any]):
        """Log data for a training trial."""
        trial_data["timestamp"] = datetime.now().isoformat()
        self.log_data["training_trials"].append(trial_data)
    
    def log_error(self, error_type: str, trial_number: int, morph_number: int, additional_data: Optional[Dict] = None):
        """Log error events (wrong key, too slow, etc.)."""
        error_data = {
            "trial_number": trial_number,
            "morph_number": morph_number,
            "timestamp": datetime.now().isoformat()
        }
        if additional_data:
            error_data.update(additional_data)
            
        if error_type == "wrong_key":
            self.log_data["errors"]["wrong_key_trials"].append(error_data)
        elif error_type == "too_slow":
            self.log_data["errors"]["too_slow_trials"].append(error_data)
    
    def calculate_experiment_summary(self, end_time: float) -> Dict[str, Any]:
        """Calculate experiment summary statistics."""
        trials = self.log_data["trials"]
        if not trials:
            return {}
        
        # Extract data for analysis
        rts = [t.get("rt", np.nan) for t in trials if t.get("rt") is not None]
        correct_responses = [t.get("correct", 0) for t in trials]
        responses = [t.get("response", np.nan) for t in trials]
        
        # Calculate statistics
        summary = {
            "experiment_time": end_time - self.log_data["start_time"],
            "total_trials": len(trials),
            "valid_rts": len([rt for rt in rts if not np.isnan(rt)]),
            "mean_rt": np.nanmean(rts) if rts else np.nan,
            "median_rt": np.nanmedian(rts) if rts else np.nan,
            "std_rt": np.nanstd(rts) if rts else np.nan,
            "accuracy": np.mean([c for c in correct_responses if c != 0]) if correct_responses else 0,
            "total_correct": sum([c for c in correct_responses if c == 1]),
            "total_incorrect": sum([c for c in correct_responses if c == -1]),
            "total_neutral": sum([c for c in correct_responses if c == 0]),
            "cumulative_reward": sum([c * self.config.reward_magnitude for c in correct_responses]),
            "wrong_key_count": len(self.log_data["errors"]["wrong_key_trials"]),
            "too_slow_count": len(self.log_data["errors"]["too_slow_trials"])
        }
        
        self.log_data["summary"] = summary
        return summary
    
    def save_log(self, subject_number: int, session: int, accumulated_winnings: float = 0):
        """Save the log data to files."""
        # Save main log file
        log_path = self.path_manager.get_log_file_path(subject_number, session)
        with open(log_path, 'w') as f:
            json.dump(self.log_data, f, indent=2, default=str)
        
        # Save accumulated winnings
        winnings_path = self.path_manager.get_accumulated_winnings_path(subject_number)
        with open(winnings_path, 'w') as f:
            json.dump({"accumulated_winnings": accumulated_winnings}, f)
        
        # Also save as CSV for easy analysis
        self._save_trials_csv(subject_number, session)
    
    def _save_trials_csv(self, subject_number: int, session: int):
        """Save trial data as CSV for easy analysis."""
        if not self.log_data["trials"]:
            return
            
        # Convert trials to DataFrame
        df = pd.DataFrame(self.log_data["trials"])
        
        # Save CSV
        csv_path = self.path_manager.get_log_file_path(subject_number, session).with_suffix('.csv')
        df.to_csv(csv_path, index=False)
    
    @classmethod
    def load_log(cls, path_manager: PathManager, subject_number: int, session: int) -> Optional[Dict[str, Any]]:
        """Load existing log data."""
        log_path = path_manager.get_log_file_path(subject_number, session)
        if log_path.exists():
            with open(log_path, 'r') as f:
                return json.load(f)
        return None
    
    @classmethod
    def load_accumulated_winnings(cls, path_manager: PathManager, subject_number: int) -> float:
        """Load accumulated winnings for a subject."""
        winnings_path = path_manager.get_accumulated_winnings_path(subject_number)
        if winnings_path.exists():
            with open(winnings_path, 'r') as f:
                data = json.load(f)
                return data.get("accumulated_winnings", 0.0)
        return 0.0


def calculate_spatial_locations(n_stimuli: int, window_rect: tuple, stimulus_size: int) -> np.ndarray:
    """
    Calculate spatial locations for N stimuli on screen.
    This replaces the locN function from MATLAB.
    
    Args:
        n_stimuli: Number of stimuli to position
        window_rect: (x, y, width, height) of the window
        stimulus_size: Size of each stimulus (assumes square)
    
    Returns:
        Array of shape (4, n_stimuli) with [left, top, right, bottom] for each stimulus
    """
    screen_width = window_rect[2] - window_rect[0]
    screen_height = window_rect[3] - window_rect[1]
    
    if n_stimuli == 3:
        # Arrange in triangle: one top, two bottom
        positions = np.zeros((4, n_stimuli))
        
        # Top stimulus (centered)
        top_x = screen_width // 2 - stimulus_size // 2
        top_y = screen_height // 4 - stimulus_size // 2
        positions[:, 0] = [top_x, top_y, top_x + stimulus_size, top_y + stimulus_size]
        
        # Bottom left stimulus
        left_x = screen_width // 4 - stimulus_size // 2
        bottom_y = 3 * screen_height // 4 - stimulus_size // 2
        positions[:, 1] = [left_x, bottom_y, left_x + stimulus_size, bottom_y + stimulus_size]
        
        # Bottom right stimulus
        right_x = 3 * screen_width // 4 - stimulus_size // 2
        positions[:, 2] = [right_x, bottom_y, right_x + stimulus_size, bottom_y + stimulus_size]
        
    else:
        # For other numbers, arrange in a row
        spacing = screen_width // (n_stimuli + 1)
        y = screen_height // 2 - stimulus_size // 2
        
        positions = np.zeros((4, n_stimuli))
        for i in range(n_stimuli):
            x = spacing * (i + 1) - stimulus_size // 2
            positions[:, i] = [x, y, x + stimulus_size, y + stimulus_size]
    
    return positions


def check_file_exists_dialog(file_path: Path) -> bool:
    """
    Check if file exists and ask user for overwrite permission.
    Similar to the file existence check in mainMRI_DiscriminationTest3.m
    
    Args:
        file_path: Path to check
        
    Returns:
        True if file should be created/overwritten, False otherwise
    """
    if not file_path.exists():
        return True
    
    try:
        from psychopy import gui
        
        info = {'Overwrite existing file? (y/n)': 'n'}
        dlg = gui.DlgFromDict(dictionary=info, title='File Exists')
        if dlg.OK:
            return info['Overwrite existing file? (y/n)'].lower() == 'y'
        else:
            return False
            
    except ImportError:
        # Fallback to command line
        response = input(f"File {file_path} already exists. Overwrite? (y/n): ")
        return response.lower() == 'y'