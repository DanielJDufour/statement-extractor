[![Build Status](https://travis-ci.org/DanielJDufour/statement-extractor.svg?branch=master)](https://travis-ci.org/DanielJDufour/statement-extractor)

# statement-extractor
statement-extractor helps you extract statements from text

# Installation
```
pip install statement-extractor
```

# Use
```
from statement_extractor import extract_statements
text = 'He said "I support you."'
statements = extract_statements(text)
print statements
# prints [{'speaker': "He", 'statement': "I support you."}]
```

# Features
| Languages Supported |
| ------------------- |
| English |

# Testing
To test the package run
```
python -m unittest statement_extractor.tests.test
