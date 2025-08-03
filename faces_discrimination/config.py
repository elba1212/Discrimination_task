"""
Configuration module for face discrimination experiments.
"""
import os
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class ExperimentConfig:
    """Configuration class for face discrimination experiments."""
    
    # Subject and session info
    subject_number: int = 999
    session: int = 1
    gender_faces: str = "m"  # 'm' for men, 'w' for women
    flip_hebrew_text: bool = True
    include_training: bool = True
    
    # Experiment parameters
    n_faces: int = 3  # Number of original faces
    n_morphs: int = 66  # Number of morphs on the axis
    repetitions: int = 6  # Number of repetitions of each trial
    training_trials: int = 6  # Number of training trials
    
    # Timing parameters (in seconds)
    morph_display_time: float = 1.5
    feedback_display_time: float = 0.2
    inter_trial_interval: float = 0.5
    response_timeout: float = 3.0
    
    # Reward parameters
    reward_magnitude: int = 1
    
    # Display parameters
    screen_number: Optional[int] = None  # None means use max available
    background_color: tuple = (0, 0, 0)  # Black background
    text_color: tuple = (255, 255, 255)  # White text
    highlight_color: tuple = (237, 177, 32)  # Orange highlight
    text_size: int = 36
    text_font: str = "Arial"
    fixation_cross_size: int = 40
    line_width: int = 4
    
    # Key mappings
    left_key: str = "left"
    right_key: str = "right" 
    down_key: str = "down"
    escape_key: str = "escape"
    
    # Instructions
    instruction_images: List[str] = field(default_factory=lambda: [
        "instructions_discrimination_MRI1",
        "instructions_discrimination_MRI2", 
        "instructions_discrimination_MRI3",
        "instructions_discrimination_MRI4"
    ])
    
    # Morph divisions - which morphs belong to which original face
    morphs_division: Dict[int, List[int]] = field(default_factory=lambda: {
        1: [1, 12, 2, 22, 13, 3, 31, 23, 14, 4, 39, 32, 24, 15, 5, 40, 33, 25, 16, 34],
        2: [11, 21, 10, 30, 20, 9, 38, 29, 19, 8, 45, 37, 28, 18, 7, 44, 36, 27, 17, 35],
        3: [66, 64, 65, 61, 62, 63, 57, 58, 59, 60, 52, 53, 54, 55, 56, 47, 48, 49, 50, 42]
    })
    
    # Hebrew text messages (as Unicode code points)
    hebrew_messages: Dict[str, List[int]] = field(default_factory=lambda: {
        "which_figure": [1489, 1495, 1512, 47, 1497, 32, 1489, 1508, 1512, 1510, 1493, 1507, 32, 1492, 1491, 1493, 1502, 1492, 32, 1489, 1497, 1493, 1514, 1512, 32, 1500, 1508, 1512, 1510, 1493, 1507, 32, 1492, 1511, 1493, 1491, 1501],
        "wrong_key": [1502, 1511, 1513, 32, 1513, 1490, 1493, 1497, 32],
        "too_slow": [1504, 1490, 1502, 1512, 32, 1492, 1494, 1502, 1503, 32],
        "winnings": [1495, 1500, 1511, 32, 1494, 1492, 32, 1492, 1505, 1514, 1497, 1497, 1501, 46, 32, 1505, 1498, 32, 1492, 1504, 1497, 1511, 1493, 1491, 32, 1513, 1510, 1489, 1512, 1514, 32, 1489, 1495, 1500, 1511, 32, 1494, 1492, 58, 32],
        "all_winnings": [1502, 1505, 1508, 1512, 32, 1492, 1504, 1511, 1493, 1491, 1493, 1514, 32, 1492, 1499, 1493, 1500, 1500, 32, 1513, 1510, 1489, 1512, 1514, 58, 32]
    })

    def get_hebrew_text(self, key: str) -> str:
        """Convert Hebrew text from Unicode code points to string."""
        codes = self.hebrew_messages.get(key, [])
        if self.flip_hebrew_text:
            codes = list(reversed(codes))
        return ''.join(chr(code) for code in codes)

    def validate(self) -> bool:
        """Validate configuration parameters."""
        if self.gender_faces not in ["m", "w"]:
            raise ValueError("gender_faces must be 'm' or 'w'")
        if self.session < 1:
            raise ValueError("session must be >= 1")
        if self.n_faces < 2:
            raise ValueError("n_faces must be >= 2")
        if self.n_morphs < 1:
            raise ValueError("n_morphs must be >= 1")
        return True

    @classmethod
    def from_dialog(cls) -> 'ExperimentConfig':
        """Create configuration from user dialog (similar to MATLAB inputdlg)."""
        try:
            from psychopy import gui
            
            info = {
                'Subject number': 999,
                'Session': 1,
                'Men/Women faces (m/w)': 'm',
                'Flip hebrew text (y/n)': 'y',
                'Training (y/n)': 'y'
            }
            
            dlg = gui.DlgFromDict(dictionary=info, title='Experiment Setup')
            if dlg.OK:
                config = cls(
                    subject_number=int(info['Subject number']),
                    session=int(info['Session']),
                    gender_faces=info['Men/Women faces (m/w)'],
                    flip_hebrew_text=info['Flip hebrew text (y/n)'].lower() == 'y',
                    include_training=info['Training (y/n)'].lower() == 'y'
                )
                config.validate()
                return config
            else:
                raise RuntimeError("User cancelled dialog")
                
        except ImportError:
            # Fallback to command line input if PsychoPy GUI not available
            print("PsychoPy GUI not available, using command line input")
            subject_number = int(input("Subject number [999]: ") or "999")
            session = int(input("Session [1]: ") or "1")
            gender_faces = input("Men/Women faces (m/w) [m]: ") or "m"
            flip_text = input("Flip hebrew text (y/n) [y]: ").lower() or "y"
            training = input("Training (y/n) [y]: ").lower() or "y"
            
            config = cls(
                subject_number=subject_number,
                session=session,
                gender_faces=gender_faces,
                flip_hebrew_text=flip_text == 'y',
                include_training=training == 'y'
            )
            config.validate()
            return config