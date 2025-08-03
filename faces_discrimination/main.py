"""
Main experiment runner for face discrimination experiments.
Converts mainMRI_DiscriminationTest3.m functionality.
"""
import sys
import traceback
from pathlib import Path
from typing import Optional

from .config import ExperimentConfig
from .utils import PathManager
from .discrimination_test import FacesDiscriminationTest


def run_experiment(config: Optional[ExperimentConfig] = None, 
                  base_path: Optional[str] = None) -> dict:
    """
    Run the face discrimination experiment.
    
    Args:
        config: Experiment configuration. If None, will be created from dialog.
        base_path: Base path for experiment files. If None, uses current directory.
        
    Returns:
        Dictionary containing experiment results
    """
    try:
        # Create configuration if not provided
        if config is None:
            config = ExperimentConfig.from_dialog()
        
        # Validate configuration
        config.validate()
        
        # Create path manager
        path_manager = PathManager(base_path)
        
        # Create and run experiment
        experiment = FacesDiscriminationTest(config, path_manager)
        results = experiment.run()
        
        return results
        
    except Exception as e:
        print(f"Error running experiment: {e}")
        traceback.print_exc()
        return {"status": "error", "error": str(e)}


def main():
    """Main entry point for command line execution."""
    try:
        print("Face Discrimination Experiment")
        print("=" * 40)
        
        # Run experiment with dialog-based configuration
        results = run_experiment()
        
        # Print results
        status = results.get("status", "unknown")
        print(f"\nExperiment status: {status}")
        
        if status == "completed":
            summary = results.get("summary", {})
            print(f"Total trials: {summary.get('total_trials', 'N/A')}")
            print(f"Mean RT: {summary.get('mean_rt', 'N/A'):.3f}s")
            print(f"Accuracy: {summary.get('accuracy', 'N/A'):.2%}")
            print(f"Cumulative reward: {summary.get('cumulative_reward', 'N/A')}")
            print(f"Accumulated winnings: {results.get('accumulated_winnings', 'N/A')}")
            
        elif status == "cancelled":
            reason = results.get("reason", "unknown")
            print(f"Cancellation reason: {reason}")
            
        elif status == "error":
            error = results.get("error", "unknown")
            print(f"Error: {error}")
            
    except KeyboardInterrupt:
        print("\nExperiment interrupted by user.")
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()