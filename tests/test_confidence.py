from parser import extract_errors
from confidence import calculate_confidence

errors = extract_errors("samples/github_failure.log")

print(calculate_confidence(errors))