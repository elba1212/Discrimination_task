"""
Main discrimination test module for face discrimination experiments.
Converts facesDiscriminationTest3.m functionality.
"""
import numpy as np
import random
from typing import Dict, List, Any, Optional, Tuple
from psychopy import visual, core, event, gui
from pathlib import Path

from .config import ExperimentConfig
from .utils import PathManager, Logger, calculate_spatial_locations
from .training import TrainingDiscriminationTest


class FacesDiscriminationTest:
    """
    Main face discrimination test.
    Equivalent to facesDiscriminationTest3.m functionality.
    """
    
    def __init__(self, config: ExperimentConfig, path_manager: PathManager):
        """
        Initialize discrimination test.
        
        Args:
            config: Experiment configuration
            path_manager: Path manager for file access
        """
        self.config = config
        self.path_manager = path_manager
        self.logger = Logger(path_manager, config)
        
        # Experiment state
        self.window = None
        self.accumulated_winnings = 0.0
        self.original_faces = []
        self.stimulus_positions = None
        
        # Trial data
        self.trial_order = []
        self.original_order = []
        self.responses = []
        self.reaction_times = []
        self.correct_responses = []
        self.subject_choices = []
        
        # Error tracking
        self.wrong_key_trials = []
        self.too_slow_trials = []
        
        # Timing
        self.start_time = None
        self.end_time = None
        
    def initialize_window(self) -> visual.Window:
        """Initialize PsychoPy window."""
        try:
            # Get screen number
            screen_num = self.config.screen_number
            if screen_num is None:
                screen_num = -1  # Use default screen
                
            # Create window
            self.window = visual.Window(
                size=(1024, 768),  # Default size, will be fullscreen
                fullscr=True,
                screen=screen_num,
                color=self.config.background_color,
                colorSpace='rgb255',
                units='pix'
            )
            
            # Set up text properties
            self.window.mouseVisible = False
            
            return self.window
            
        except Exception as e:
            print(f"Error initializing window: {e}")
            raise
    
    def setup_experiment(self) -> bool:
        """
        Set up experiment parameters and check for existing data.
        
        Returns:
            True if setup successful, False if user cancelled
        """
        # Check if log file already exists
        log_path = self.path_manager.get_log_file_path(
            self.config.subject_number, 
            self.config.session
        )
        
        if log_path.exists():
            from .utils import check_file_exists_dialog
            if not check_file_exists_dialog(log_path):
                return False
        
        # Load accumulated winnings if session > 1
        if self.config.session == 2:
            # For session 2, ask user for accumulated winnings from learning task
            try:
                from psychopy import gui
                info = {'Accumulated winnings from learning task': '0'}
                dlg = gui.DlgFromDict(dictionary=info, title='Previous Winnings')
                if dlg.OK:
                    self.accumulated_winnings = float(info['Accumulated winnings from learning task'])
                else:
                    return False
            except (ImportError, ValueError):
                try:
                    self.accumulated_winnings = float(input("Enter accumulated winnings from learning task: "))
                except ValueError:
                    self.accumulated_winnings = 0.0
                    
        elif self.config.session >= 3:
            # Load from previous session
            self.accumulated_winnings = Logger.load_accumulated_winnings(
                self.path_manager, self.config.subject_number
            )
        else:
            self.accumulated_winnings = 0.0
        
        # Set original faces
        if self.config.session > 1:
            # Load original faces from session 1
            session1_log = Logger.load_log(
                self.path_manager, self.config.subject_number, 1
            )
            if session1_log:
                self.original_faces = session1_log.get("faces", [1, 2, 3])
            else:
                print("Warning: Could not load session 1 data, using default faces")
                self.original_faces = [1, 2, 3]
        else:
            # First session - randomize face order
            faces = list(range(1, self.config.n_faces + 1))
            self.original_faces = random.sample(faces, self.config.n_faces)
        
        # Setup stimulus positions
        self._setup_stimulus_positions()
        
        return True
    
    def _setup_stimulus_positions(self):
        """Setup spatial positions for stimuli."""
        if self.window is None:
            return
            
        # Get window size
        win_size = self.window.size
        window_rect = (0, 0, win_size[0], win_size[1])
        
        # Calculate positions
        self.stimulus_positions = calculate_spatial_locations(
            n_stimuli=self.config.n_faces,
            window_rect=window_rect,
            stimulus_size=200
        )
    
    def show_instructions(self) -> bool:
        """
        Show experiment instructions.
        
        Returns:
            True if user wants to continue, False if escape was pressed
        """
        instruction_index = 0
        
        while instruction_index < len(self.config.instruction_images):
            try:
                # Load instruction image
                instruction_name = self.config.instruction_images[instruction_index]
                instruction_path = self.path_manager.get_instruction_path(instruction_name)
                
                if instruction_path.exists():
                    instruction_stim = visual.ImageStim(
                        self.window,
                        image=str(instruction_path),
                        units='pix'
                    )
                    instruction_stim.draw()
                else:
                    # Fallback text
                    instruction_text = visual.TextStim(
                        self.window,
                        text=f"Instruction {instruction_index + 1}\n\n"
                             "Face discrimination experiment\n\n"
                             "You will see a face, then choose which of the original faces "
                             "is most similar to it.\n\n"
                             "Left arrow: Previous\nRight arrow: Next\nEscape: Exit",
                        height=30,
                        color=self.config.text_color,
                        wrapWidth=800
                    )
                    instruction_text.draw()
                
                self.window.flip()
                core.wait(0.2)  # Brief wait to prevent key bounce
                
                # Wait for key press
                keys = event.waitKeys(keyList=['left', 'right', 'escape'])
                
                if 'escape' in keys:
                    return False
                elif 'left' in keys:
                    if instruction_index > 0:
                        instruction_index -= 1
                    else:
                        instruction_index += 1  # Can't go back from first instruction
                elif 'right' in keys:
                    instruction_index += 1
                    
                core.wait(0.1)  # Brief wait
                
            except Exception as e:
                print(f"Error showing instruction {instruction_index}: {e}")
                instruction_index += 1
        
        return True
    
    def show_break_screen(self):
        """Show break screen between instructions and experiment."""
        try:
            break_path = self.path_manager.get_instruction_path("instructions_break")
            
            if break_path.exists():
                break_stim = visual.ImageStim(
                    self.window,
                    image=str(break_path),
                    units='pix'
                )
                break_stim.draw()
            else:
                break_text = visual.TextStim(
                    self.window,
                    text="Get ready to start the experiment!\n\nPress any key when ready...",
                    height=40,
                    color=self.config.text_color
                )
                break_text.draw()
                
            self.window.flip()
            event.waitKeys()
            
        except Exception as e:
            print(f"Error showing break screen: {e}")
    
    def run_training(self) -> bool:
        """
        Run training session if enabled.
        
        Returns:
            True if training completed or skipped, False if user cancelled
        """
        if not self.config.include_training:
            return True
            
        training = TrainingDiscriminationTest(
            self.config, self.path_manager, self.window, self.logger
        )
        
        return training.run()
    
    def setup_trials(self):
        """Setup trial order and parameters."""
        # Create trial list
        trials = []
        for _ in range(self.config.repetitions):
            trials.extend(range(1, self.config.n_morphs + 1))
        
        # Shuffle trials
        indices = list(range(len(trials)))
        random.shuffle(indices)
        
        self.trial_order = [trials[i] for i in indices]
        
        # Calculate original order for unshuffling results
        self.original_order = [0] * len(trials)
        for new_pos, old_pos in enumerate(indices):
            self.original_order[old_pos] = new_pos
    
    def run_experiment_trials(self) -> bool:
        """
        Run the main experiment trials.
        
        Returns:
            True if completed successfully, False if aborted
        """
        n_trials = len(self.trial_order)
        
        for trial_idx in range(n_trials):
            # Show break in middle of experiment
            if trial_idx == n_trials // 2:
                self._show_mid_experiment_break()
            
            # Run single trial
            success = self._run_single_trial(trial_idx)
            
            if success is None:  # Escape pressed
                return False
            elif success in ["wrong_key", "too_slow"]:
                # Error occurred but continue experiment
                continue
                
        return True
    
    def _show_mid_experiment_break(self):
        """Show break screen in middle of experiment."""
        try:
            break_path = self.path_manager.get_instruction_path("break")
            
            if break_path.exists():
                break_stim = visual.ImageStim(
                    self.window,
                    image=str(break_path),
                    units='pix'
                )
                break_stim.draw()
            else:
                break_text = visual.TextStim(
                    self.window,
                    text="Break time!\n\nTake a short rest.\n\nPress any key to continue...",
                    height=40,
                    color=self.config.text_color
                )
                break_text.draw()
                
            self.window.flip()
            event.waitKeys()
            
        except Exception as e:
            print(f"Error showing mid-experiment break: {e}")
    
    def _run_single_trial(self, trial_idx: int) -> Optional[str]:
        """
        Run a single experiment trial.
        
        Args:
            trial_idx: Index of current trial
            
        Returns:
            "success", "wrong_key", "too_slow", or None (escape)
        """
        morph_num = self.trial_order[trial_idx]
        
        # Phase 1: Show morph
        morph_path = self.path_manager.get_morph_path(
            self.config.gender_faces, morph_num
        )
        
        if morph_path.exists():
            morph_stim = visual.ImageStim(
                self.window,
                image=str(morph_path),
                units='pix'
            )
            morph_stim.draw()
        else:
            # Fallback placeholder
            placeholder = visual.TextStim(
                self.window,
                text=f"Morph {morph_num}",
                height=50,
                color=self.config.text_color
            )
            placeholder.draw()
            
        self.window.flip()
        core.wait(self.config.morph_display_time)
        
        # Phase 2: Show choice phase
        return self._run_choice_phase(trial_idx, morph_num)
    
    def _run_choice_phase(self, trial_idx: int, morph_num: int) -> Optional[str]:
        """Run the choice phase of a trial."""
        # Load original face images
        original_stims = []
        
        for i, original_num in enumerate(self.original_faces):
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
            pos=(0, 250)
        )
        
        # Draw all stimuli
        instruction_text.draw()
        for stim in original_stims:
            stim.draw()
            
        self.window.flip()
        
        # Collect response
        return self._collect_trial_response(trial_idx, morph_num, original_stims)
    
    def _collect_trial_response(self, trial_idx: int, morph_num: int,
                               original_stims: List[visual.BaseVisualStim]) -> Optional[str]:
        """Collect and process response for main experiment trial."""
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
            self.logger.log_error("too_slow", trial_idx, morph_num)
            return "too_slow"
            
        key, rt = keys[0]
        
        if key == 'escape':
            return None
            
        # Process valid responses
        if key in ['left', 'down', 'right']:
            response_mapping = {'left': 1, 'down': 2, 'right': 3}
            response = response_mapping[key]
            
            # Calculate correctness
            subject_choice = self.original_faces[response - 1]
            correct = self._calculate_correctness(morph_num, subject_choice)
            
            # Store trial data
            trial_data = {
                "trial_index": trial_idx,
                "morph_number": morph_num,
                "response": response,
                "subject_choice": subject_choice,
                "correct": correct,
                "rt": rt,
                "key_pressed": key
            }
            
            # Log the trial
            self.logger.log_trial(trial_data)
            
            # Show feedback
            self._show_response_feedback(response, original_stims)
            
            return "success"
        else:
            # Wrong key pressed
            self._show_feedback("wrong_key")
            self.logger.log_error("wrong_key", trial_idx, morph_num)
            return "wrong_key"
    
    def _calculate_correctness(self, morph_num: int, subject_choice: int) -> int:
        """
        Calculate if response was correct based on morph divisions.
        
        Args:
            morph_num: The morph number shown
            subject_choice: The face number chosen by subject
            
        Returns:
            1 if correct, -1 if incorrect, 0 if neutral/ambiguous
        """
        # Check which original face this morph belongs to
        for original_face, morphs in self.config.morphs_division.items():
            if morph_num in morphs:
                if subject_choice == original_face:
                    return 1  # Correct
                else:
                    return -1  # Incorrect
        
        # If morph not found in any division, consider neutral
        return 0
    
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
        
        # Inter-trial interval
        self.window.flip()  # Clear screen
        core.wait(self.config.inter_trial_interval)
    
    def _show_feedback(self, feedback_type: str):
        """Show feedback message for errors."""
        if feedback_type == "wrong_key":
            message = self.config.get_hebrew_text("wrong_key")
        elif feedback_type == "too_slow":
            message = self.config.get_hebrew_text("too_slow")
        else:
            message = "Error"
            
        feedback_text = visual.TextStim(
            self.window,
            text=message,
            height=self.config.text_size,
            color=self.config.text_color
        )
        
        feedback_text.draw()
        self.window.flip()
        core.wait(1.0)
    
    def _get_stimulus_position(self, index: int) -> tuple:
        """Get the position for stimulus at given index."""
        if self.stimulus_positions is None:
            return (0, 0)
            
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
    
    def show_results(self):
        """Show experiment results and winnings."""
        # Calculate session reward
        trials = self.logger.log_data.get("trials", [])
        session_reward = sum([
            t.get("correct", 0) * self.config.reward_magnitude 
            for t in trials
        ])
        
        # Update accumulated winnings
        self.accumulated_winnings += session_reward
        
        # Show session winnings
        session_text = (
            self.config.get_hebrew_text("winnings") + 
            str(session_reward)
        )
        
        winnings_stim = visual.TextStim(
            self.window,
            text=session_text,
            height=self.config.text_size,
            color=self.config.text_color
        )
        winnings_stim.draw()
        self.window.flip()
        core.wait(3.0)
        
        # Show accumulated winnings
        total_text = (
            self.config.get_hebrew_text("all_winnings") + 
            str(self.accumulated_winnings)
        )
        
        total_stim = visual.TextStim(
            self.window,
            text=total_text,
            height=self.config.text_size,
            color=self.config.text_color
        )
        total_stim.draw()
        self.window.flip()
        core.wait(3.0)
    
    def cleanup(self):
        """Clean up resources."""
        if self.window:
            self.window.mouseVisible = True
            self.window.close()
    
    def run(self) -> Dict[str, Any]:
        """
        Run the complete discrimination test.
        
        Returns:
            Dictionary containing experiment results and log data
        """
        try:
            # Initialize window
            self.initialize_window()
            
            # Setup experiment
            if not self.setup_experiment():
                return {"status": "cancelled", "reason": "user_cancelled_setup"}
            
            # Initialize logging
            self.start_time = core.getTime()
            self.logger.initialize_log(self.start_time, self.original_faces)
            
            # Show instructions
            if not self.show_instructions():
                return {"status": "cancelled", "reason": "user_cancelled_instructions"}
            
            # Show break screen
            self.show_break_screen()
            
            # Run training if enabled
            if not self.run_training():
                return {"status": "cancelled", "reason": "user_cancelled_training"}
            
            # Setup trials
            self.setup_trials()
            
            # Run main experiment
            if not self.run_experiment_trials():
                return {"status": "cancelled", "reason": "user_cancelled_experiment"}
            
            # Record end time
            self.end_time = core.getTime()
            
            # Calculate summary
            summary = self.logger.calculate_experiment_summary(self.end_time)
            
            # Show results
            self.show_results()
            
            # Save data
            self.logger.save_log(
                self.config.subject_number,
                self.config.session,
                self.accumulated_winnings
            )
            
            return {
                "status": "completed",
                "summary": summary,
                "accumulated_winnings": self.accumulated_winnings,
                "log_data": self.logger.log_data
            }
            
        except Exception as e:
            print(f"Error during experiment: {e}")
            return {"status": "error", "error": str(e)}
            
        finally:
            self.cleanup()