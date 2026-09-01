import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from parser import extract_errors
from rule_engine import check_known_errors

errors = extract_errors("samples/github_failure.log")

result = check_known_errors(errors)

print(result)