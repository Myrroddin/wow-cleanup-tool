import os
import sys
import unittest

# Ensure src/ is in PYTHONPATH for module discovery
SRC_PATH = os.path.join(os.path.dirname(__file__), 'src')
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover(SRC_PATH)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())