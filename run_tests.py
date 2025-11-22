import sys
import pytest
from tests import test_models

def run_tests():
    # Manually run functions starting with test_
    functions = [func for name, func in vars(test_models).items() if name.startswith("test_") and callable(func)]
    
    passed = 0
    failed = 0
    
    print(f"Running {len(functions)} tests...")
    
    for func in functions:
        try:
            func()
            print(f"[PASS] {func.__name__}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {func.__name__}")
            import traceback
            with open("test_results.log", "a") as f:
                f.write(f"Error in {func.__name__}:\n")
                traceback.print_exc(file=f)
                f.write("\n")
            print(f"Error logged to test_results.log")
            failed += 1
            
    print(f"\nSummary: {passed} passed, {failed} failed.")
    
    if failed > 0:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    run_tests()
