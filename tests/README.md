# Running Tests

This directory contains tests for the keycloak-extensions handler module. Follow these steps to run the tests:

## Setup

1. Create a virtual environment:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```

2. Install the development requirements:

```bash
# Make sure you're in the handler directory with the virtual environment activated
pip install -r tests/requirements.txt
```

## Running Tests

To run all tests:

```bash
# Make sure the virtual environment is activated
pytest tests/handler
```

To run a specific test file:

```bash
pytest tests/handler/test_notifier.py
```

To run a specific test:

```bash
pytest tests/handler/test_notifier.py::test_notify_new_logins
```

To show output during test execution:

```bash
pytest tests/handler/test_notifier.py -v
```

## Debug Output

To show print statements and other output during tests:

```bash
pytest tests/handler/test_notifier.py -s
```

## Troubleshooting

If you encounter module import errors, you may need to set the `PYTHONPATH` environment variable:

```bash
# On Linux/macOS:
PYTHONPATH=$(pwd) pytest tests/handler/
```
