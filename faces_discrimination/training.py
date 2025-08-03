"""
Training module for face discrimination experiments.
Converts TrainingDiscriminationTest3.m functionality.
"""
import numpy as np
from typing import Dict, List, Any, Optional
from psychopy import visual, core, event, gui
from pathlib import Path

from .config import ExperimentConfig
from .utils import PathManager, Logger


class TrainingDiscriminationTest:
    """
    Training session for face discrimination experiment.
    Equivalent to TrainingDiscriminationTest3.m functionality.
    """
    
    def __init__(self, config: ExperimentConfig, path_manager: PathManager, 
                 window: visual.Window, logger: Logger):
        """
        Initialize training session.
        
        Args:
            config: Experiment configuration
            path_manager: Path manager for file access
            window: PsychoPy window object
            logger: Logger instance
        """
        self.config = config
        self.path_manager = path_manager
        self.window = window
        self.logger = logger
        
        # Training-specific parameters
        self.n_training_trials = config.training_trials
        self.originals = [1, 2, 3]  # Training uses faces 1, 2, 3
        
        # Stimulus positions
        self._setup_stimulus_positions()
        
        # Response tracking
        self.responses = []
        self.reaction_times = []
        self.wrong_key_trials = []
        self.too_slow_trials = []
        
    def _setup_stimulus_positions(self):
        """Setup spatial positions for stimuli."""
        from .utils import calculate_spatial_locations
        
        # Get window size
        win_size = self.window.size
        window_rect = (0, 0, win_size[0], win_size[1])
        
        # Calculate positions for 3 stimuli
        self.stimulus_positions = calculate_spatial_locations(
            n_stimuli=3, 
            window_rect=window_rect, 
            stimulus_size=200  # Approximate stimulus size
        )
        
    def show_instructions(self) -> bool:
        """
        Show training instructions.
        
        Returns:
            True if user wants to continue, False if escape was pressed
        """
        try:
            # Load instruction image
            instruction_path = self.path_manager.get_instruction_path("instructions_discrimination_MRI5")
            
            if instruction_path.exists():
                instruction_stim = visual.ImageStim(
                    self.window,
                    image=str(instruction_path),
                    units='pix'
                )
                instruction_stim.draw()
            else:
                # Fallback text if image doesn't exist
                instruction_text = visual.TextStim(
                    self.window,
                    text="Training Instructions:\n\n"
                         "You will see a face, then choose which of the 3 original faces "
                         "is most similar to it.\n\n"
                         "Use LEFT, DOWN, and RIGHT arrow keys to respond.\n\n"
                         "Press any key to continue...",
                    height=30,
                    color=self.config.text_color,
                    wrapWidth=800
                )
                instruction_text.draw()
            
            self.window.flip()
            
            # Wait for key press
            keys = event.waitKeys(keyList=['left', 'right', 'down', 'escape'])
            
            if 'escape' in keys:
                return False
                
            return True
            
        except Exception as e:
            print(f"Error showing instructions: {e}")
            return True
    
    def run_training_loop(self) -> bool:
        """
        Run the main training loop.
        
        Returns:
            True if training completed successfully, False if aborted
        """
        trial = 0
        wrong_key_count = 0
        too_slow_count = 0
        
        while trial < self.n_training_trials:
            # Show morph stimulus
            morph_num = trial + 1  # Training uses morphs 1-6
            
            success = self._run_single_trial(trial, morph_num)
            
            if success is None:  # Escape pressed
                return False
            elif success == "wrong_key":
                self.wrong_key_trials.append({
                    "trial": trial,
                    "morph": morph_num
                })
                wrong_key_count += 1
                continue  # Don't advance trial
            elif success == "too_slow":
                self.too_slow_trials.append({
                    "trial": trial, 
                    "morph": morph_num
                })
                too_slow_count += 1
                continue  # Don't advance trial
            else:
                trial += 1  # Advance to next trial
                
        return True
    
    def _run_single_trial(self, trial_num: int, morph_num: int) -> Optional[str]:
        """
        Run a single training trial.
        
        Args:
            trial_num: Trial number
            morph_num: Morph number to display
            
        Returns:
            "success", "wrong_key", "too_slow", or None (escape)
        """
        # Phase 1: Show morph
        morph_path = self.path_manager.get_training_morph_path(morph_num)
        
        if morph_path.exists():
            morph_stim = visual.ImageStim(
                self.window,
                image=str(morph_path),
                units='pix'
            )
            morph_stim.draw()
        else:
            # Fallback if image doesn't exist
            placeholder = visual.TextStim(
                self.window,
                text=f"Morph {morph_num}",
                height=50,
                color=self.config.text_color
            )
            placeholder.draw()
            
        self.window.flip()
        core.wait(self.config.morph_display_time)
        
        # Phase 2: Show original faces for choice
        return self._show_choice_phase(trial_num, morph_num)
    
    def _show_choice_phase(self, trial_num: int, morph_num: int) -> Optional[str]:
        """
        Show the choice phase with original faces.
        
        Args:
            trial_num: Trial number
            morph_num: Morph number that was shown
            
        Returns:
            "success", "wrong_key", "too_slow", or None (escape)
        """
        # Load original face images
        original_stims = []
        
        for i, original_num in enumerate(self.originals):
            original_path = self.path_manager.get_original_path(
                self.config.gender_faces, original_num
            )
            
            if original_path.exists():
                stim = visual.ImageStim(
                    self.window,
                    image=str(original_path),
                    units='pix',
                    pos=self._get_stimulus_position(i)
                )
                original_stims.append(stim)
            else:
                # Fallback placeholder
                stim = visual.TextStim(
                    self.window,
                    text=f"Face {original_num}",
                    height=30,
                    color=self.config.text_color,
                    pos=self._get_stimulus_position(i)
                )
                original_stims.append(stim)
        
        # Show instruction text
        instruction_text = visual.TextStim(
            self.window,
            text=self.config.get_hebrew_text("which_figure"),
            height=self.config.text_size,
            color=self.config.text_color,
            pos=(0, 200)
        )
        
        # Draw all stimuli
        instruction_text.draw()
        for stim in original_stims:
            stim.draw()
            
        self.window.flip()
        
        # Collect response
        return self._collect_response(trial_num, morph_num, original_stims)
    
    def _collect_response(self, trial_num: int, morph_num: int, 
                         original_stims: List[visual.BaseVisualStim]) -> Optional[str]:
        """
        Collect and process user response.
        
        Args:
            trial_num: Trial number
            morph_num: Morph number
            original_stims: List of original face stimuli
            
        Returns:
            "success", "wrong_key", "too_slow", or None (escape)
        """
        # Clear event buffer
        event.clearEvents()
        
        # Start timer
        response_clock = core.Clock()
        
        # Wait for response
        keys = event.waitKeys(
            maxWait=self.config.response_timeout,
            keyList=['left', 'down', 'right', 'escape'],
            timeStamped=response_clock
        )
        
        if not keys:
            # No response (too slow)
            self._show_feedback("too_slow")
            return "too_slow"
            
        key, rt = keys[0]
        
        if key == 'escape':
            return None
            
        # Process valid responses
        if key in ['left', 'down', 'right']:
            response_mapping = {'left': 1, 'down': 2, 'right': 3}
            response = response_mapping[key]
            
            # Log the response
            trial_data = {
                "trial_number": trial_num,
                "morph_number": morph_num,
                "response": response,
                "rt": rt,
                "key_pressed": key
            }
            
            self.responses.append(response)
            self.reaction_times.append(rt)
            self.logger.log_training_trial(trial_data)
            
            # Show feedback (highlight chosen stimulus)
            self._show_response_feedback(response, original_stims)
            
            return "success"
        else:
            # Wrong key pressed
            self._show_feedback("wrong_key")
            return "wrong_key"
    
    def _show_response_feedback(self, response: int, original_stims: List[visual.BaseVisualStim]):
        """Show feedback highlighting the chosen stimulus."""
        # Highlight the chosen stimulus
        highlight_pos = self._get_stimulus_position(response - 1)
        
        # Create highlight rectangle
        highlight_rect = visual.Rect(
            self.window,
            width=220, height=220,
            pos=highlight_pos,
            lineColor=self.config.highlight_color,
            lineWidth=8,
            fillColor=None
        )
        
        # Redraw everything with highlight
        for stim in original_stims:
            stim.draw()
        highlight_rect.draw()
        
        self.window.flip()
        core.wait(self.config.feedback_display_time)
    
    def _show_feedback(self, feedback_type: str):
        """Show feedback message for wrong key or too slow responses."""
        if feedback_type == "wrong_key":
            message = self.config.get_hebrew_text("wrong_key")
        elif feedback_type == "too_slow":
            message = self.config.get_hebrew_text("too_slow")
        else:
            message = "Unknown error"
            
        feedback_text = visual.TextStim(
            self.window,
            text=message,
            height=self.config.text_size,
            color=self.config.text_color
        )
        
        feedback_text.draw()
        self.window.flip()
        core.wait(1.0)  # Show feedback for 1 second
    
    def _get_stimulus_position(self, index: int) -> tuple:
        """Get the position for stimulus at given index."""
        # Convert from pixel coordinates to PsychoPy coordinates
        win_size = self.window.size
        
        # Calculate position relative to window center
        pixel_pos = self.stimulus_positions[:, index]
        center_x = pixel_pos[0] + (pixel_pos[2] - pixel_pos[0]) / 2
        center_y = pixel_pos[1] + (pixel_pos[3] - pixel_pos[1]) / 2
        
        # Convert to PsychoPy coordinates (center at 0,0)
        psychopy_x = center_x - win_size[0] / 2
        psychopy_y = win_size[1] / 2 - center_y
        
        return (psychopy_x, psychopy_y)
    
    def show_end_screen(self) -> bool:
        """
        Show training end screen and ask if user wants to repeat.
        
        Returns:
            True if user wants to continue, False if wants to repeat training
        """
        try:
            # Load end screen image
            end_screen_path = self.path_manager.get_instruction_path("training_end_dis")
            
            if end_screen_path.exists():
                end_screen_stim = visual.ImageStim(
                    self.window,
                    image=str(end_screen_path),
                    units='pix'
                )
                end_screen_stim.draw()
            else:
                # Fallback text
                end_text = visual.TextStim(
                    self.window,
                    text="Training Complete!\n\n"
                         "Left arrow: Continue to main experiment\n"
                         "Right arrow: Repeat training\n"
                         "Escape: Exit",
                    height=30,
                    color=self.config.text_color,
                    wrapWidth=800
                )
                end_text.draw()
                
            self.window.flip()
            
            # Wait for response
            keys = event.waitKeys(keyList=['left', 'right', 'escape'])
            
            if 'escape' in keys:
                return None
            elif 'left' in keys:
                return True  # Continue to main experiment
            else:  # 'right' in keys
                return False  # Repeat training
                
        except Exception as e:
            print(f"Error showing end screen: {e}")
            return True
    
    def run(self) -> bool:
        """
        Run the complete training session.
        
        Returns:
            True if training completed and user wants to continue,
            False if user wants to repeat or exit
        """
        done_training = False
        
        while not done_training:
            # Show instructions
            if not self.show_instructions():
                return False  # User pressed escape
            
            # Run training trials
            if not self.run_training_loop():
                return False  # User pressed escape
                
            # Show end screen and get user choice
            choice = self.show_end_screen()
            if choice is None:
                return False  # User pressed escape
            elif choice:
                done_training = True  # User wants to continue
            # If choice is False, repeat training (continue loop)
            
        return True