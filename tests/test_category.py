from parser import extract_errors
from categorizer import categorize

errors = extract_errors("samples/github_failure.log")

print(categorize(errors))