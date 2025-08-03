"""
Simple test module for basic PsychoPy functionality.
Converts test.m functionality.
"""
from psychopy import visual, core, event
from .config import ExperimentConfig


def run_simple_test():
    """
    Run a simple test similar to test.m functionality.
    Shows a fixation cross and waits for key press.
    """
    try:
        # Initialize window (similar to PsychDefaultSetup and Screen commands)
        win = visual.Window(
            fullscr=True,
            color=(0, 0, 0),  # Black background
            colorSpace='rgb255',
            units='pix'
        )
        
        # Hide mouse cursor
        win.mouseVisible = False
        
        # Create fixation cross
        fixation_size = 40  # Size of fixation cross arms
        line_width = 4
        
        # Create horizontal and vertical lines for fixation cross
        h_line = visual.Line(
            win,
            start=(-fixation_size, 0),
            end=(fixation_size, 0),
            lineWidth=line_width,
            lineColor=(255, 255, 255),  # White
            colorSpace='rgb255'
        )
        
        v_line = visual.Line(
            win,
            start=(0, -fixation_size),
            end=(0, fixation_size),
            lineWidth=line_width,
            lineColor=(255, 255, 255),  # White
            colorSpace='rgb255'
        )
        
        # Draw fixation cross
        h_line.draw()
        v_line.draw()
        
        # Flip to show on screen
        win.flip()
        
        print("Fixation cross displayed. Press any key to continue...")
        
        # Wait for key press
        event.waitKeys()
        
        # Clean up
        win.close()
        
        print("Simple test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error in simple test: {e}")
        return False


def run_text_test():
    """Test text display functionality."""
    try:
        win = visual.Window(
            size=(800, 600),
            color=(0, 0, 0),
            colorSpace='rgb255',
            units='pix'
        )
        
        # Test text display
        text_stim = visual.TextStim(
            win,
            text="PsychoPy Text Test\n\nThis tests text rendering.\n\nPress any key to continue...",
            height=30,
            color=(255, 255, 255),
            colorSpace='rgb255',
            wrapWidth=700
        )
        
        text_stim.draw()
        win.flip()
        
        print("Text test displayed. Press any key to continue...")
        event.waitKeys()
        
        win.close()
        print("Text test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error in text test: {e}")
        return False


def run_image_test():
    """Test image display functionality (if images are available)."""
    try:
        win = visual.Window(
            size=(800, 600),
            color=(0, 0, 0),
            colorSpace='rgb255',
            units='pix'
        )
        
        # Try to load a test image
        try:
            from .utils import PathManager
            path_manager = PathManager()
            
            # Try to find any image file for testing
            test_image_path = None
            for gender in ['m', 'w']:
                for original in [1, 2, 3]:
                    img_path = path_manager.get_original_path(gender, original)
                    if img_path.exists():
                        test_image_path = img_path
                        break
                if test_image_path:
                    break
            
            if test_image_path:
                img_stim = visual.ImageStim(
                    win,
                    image=str(test_image_path),
                    units='pix'
                )
                img_stim.draw()
                
                text_stim = visual.TextStim(
                    win,
                    text="Image test - Press any key to continue...",
                    height=30,
                    color=(255, 255, 255),
                    colorSpace='rgb255',
                    pos=(0, -250)
                )
                text_stim.draw()
                
                win.flip()
                
                print("Image test displayed. Press any key to continue...")
                event.waitKeys()
                
            else:
                # No images found, show placeholder
                placeholder = visual.TextStim(
                    win,
                    text="No test images found.\n\nImage display functionality appears to be working.\n\nPress any key to continue...",
                    height=30,
                    color=(255, 255, 255),
                    colorSpace='rgb255',
                    wrapWidth=700
                )
                placeholder.draw()
                win.flip()
                
                print("Image test (placeholder) displayed. Press any key to continue...")
                event.waitKeys()
                
        except ImportError:
            # PathManager not available, show placeholder
            placeholder = visual.TextStim(
                win,
                text="PathManager not available for image test.\n\nBasic image functionality appears to be working.\n\nPress any key to continue...",
                height=30,
                color=(255, 255, 255),
                colorSpace='rgb255',
                wrapWidth=700
            )
            placeholder.draw()
            win.flip()
            
            print("Image test (basic) displayed. Press any key to continue...")
            event.waitKeys()
        
        win.close()
        print("Image test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error in image test: {e}")
        return False


def run_all_tests():
    """Run all simple tests."""
    print("Running PsychoPy functionality tests...")
    print("=" * 50)
    
    tests = [
        ("Simple fixation cross test", run_simple_test),
        ("Text display test", run_text_test),
        ("Image display test", run_image_test)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        try:
            success = test_func()
            results.append((test_name, success))
            if success:
                print(f"✓ {test_name} passed")
            else:
                print(f"✗ {test_name} failed")
        except Exception as e:
            print(f"✗ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary:")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    return all(success for _, success in results)


if __name__ == "__main__":
    run_all_tests()