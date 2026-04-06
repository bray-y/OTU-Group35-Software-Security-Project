import os
import shutil

if os.path.exists("security_tests/outputs"):
    shutil.rmtree("security_tests/outputs")

print("Outputs reset")