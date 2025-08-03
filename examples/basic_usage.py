#!/usr/bin/env python3
"""
Basic usage example for the faces discrimination experiment package.

This example shows how to run the experiment with default settings,
custom configuration, and how to analyze the results.
"""

import sys
from pathlib import Path

# Add the package to path if running from examples directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from faces_discrimination import run_experiment, ExperimentConfig
from faces_discrimination.utils import PathManager, Logger


def example_basic_usage():
    """Run experiment with default settings and dialog configuration."""
    print("Example 1: Basic usage with dialog configuration")
    print("-" * 50)
    
    # Run with default settings - will show dialog for configuration
    results = run_experiment()
    
    # Print results
    print(f"Experiment status: {results.get('status')}")
    if results.get('status') == 'completed':
        summary = results.get('summary', {})
        print(f"Total trials: {summary.get('total_trials')}")
        print(f"Mean reaction time: {summary.get('mean_rt', 0):.3f}s")
        print(f"Accuracy: {summary.get('accuracy', 0):.2%}")
        print(f"Total reward: {summary.get('cumulative_reward')}")


def example_custom_config():
    """Run experiment with custom configuration."""
    print("\nExample 2: Custom configuration")
    print("-" * 50)
    
    # Create custom configuration
    config = ExperimentConfig(
        subject_number=123,
        session=1,
        gender_faces="w",  # Use women faces
        flip_hebrew_text=False,
        include_training=False,  # Skip training
        repetitions=2,  # Fewer repetitions for demo
        n_morphs=10,    # Fewer morphs for demo
        response_timeout=5.0  # Longer timeout
    )
    
    # Run experiment with custom config
    results = run_experiment(config=config)
    
    print(f"Experiment status: {results.get('status')}")
    return results


def example_analyze_results():
    """Example of how to analyze saved results."""
    print("\nExample 3: Analyzing saved results")
    print("-" * 50)
    
    # Initialize path manager
    path_manager = PathManager()
    
    # Load results from a specific subject and session
    subject_number = 123
    session = 1
    
    log_data = Logger.load_log(path_manager, subject_number, session)
    
    if log_data:
        print(f"Loaded data for subject {subject_number}, session {session}")
        
        # Analyze trial data
        trials = log_data.get("trials", [])
        if trials:
            import numpy as np
            
            # Extract reaction times and accuracy
            rts = [t.get("rt") for t in trials if t.get("rt") is not None]
            correct_responses = [t.get("correct", 0) for t in trials]
            
            print(f"Number of trials: {len(trials)}")
            print(f"Mean RT: {np.mean(rts):.3f}s")
            print(f"RT std: {np.std(rts):.3f}s")
            print(f"Accuracy: {np.mean([c for c in correct_responses if c != 0]):.2%}")
            
            # Analyze by morph number
            morph_accuracy = {}
            for trial in trials:
                morph_num = trial.get("morph_number")
                correct = trial.get("correct", 0)
                if morph_num not in morph_accuracy:
                    morph_accuracy[morph_num] = []
                morph_accuracy[morph_num].append(correct)
            
            print("\nAccuracy by morph:")
            for morph_num in sorted(morph_accuracy.keys())[:5]:  # Show first 5
                acc = np.mean([c for c in morph_accuracy[morph_num] if c != 0])
                print(f"  Morph {morph_num}: {acc:.2%}")
                
        # Check for errors
        errors = log_data.get("errors", {})
        wrong_keys = errors.get("wrong_key_trials", [])
        too_slow = errors.get("too_slow_trials", [])
        
        print(f"\nErrors:")
        print(f"  Wrong key presses: {len(wrong_keys)}")
        print(f"  Too slow responses: {len(too_slow)}")
        
    else:
        print(f"No data found for subject {subject_number}, session {session}")


def example_test_system():
    """Test system functionality."""
    print("\nExample 4: Testing system functionality")
    print("-" * 50)
    
    from faces_discrimination.test_simple import run_all_tests
    
    # Run basic system tests
    success = run_all_tests()
    
    if success:
        print("\n✓ All system tests passed!")
    else:
        print("\n✗ Some system tests failed. Check PsychoPy installation.")


def main():
    """Run all examples."""
    print("Face Discrimination Experiment - Usage Examples")
    print("=" * 60)
    
    try:
        # Example 1: Basic usage (commented out as it requires user interaction)
        # example_basic_usage()
        
        # Example 2: Custom configuration (commented out as it requires display)
        # results = example_custom_config()
        
        # Example 3: Analyze results (will work if data exists)
        example_analyze_results()
        
        # Example 4: Test system
        example_test_system()
        
        print("\n" + "=" * 60)
        print("Examples completed!")
        print("\nTo run the actual experiment:")
        print("  python -m faces_discrimination.main")
        print("\nOr programmatically:")
        print("  from faces_discrimination import run_experiment")
        print("  results = run_experiment()")
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure you have installed the required dependencies:")
        print("  pip install -r requirements.txt")
        
    except Exception as e:
        print(f"Error running examples: {e}")


if __name__ == "__main__":
    main()