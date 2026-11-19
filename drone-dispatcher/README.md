# Drone Dispatcher

The project targets Python 3.11 and uses Ruff for linting and formatting.

From the `Refactoring` repository root, install the development tools and enable
the local Git hook:

```powershell
python -m pip install -r drone-dispatcher/requirements-dev.txt
python -m pre_commit install --config drone-dispatcher/.pre-commit-config.yaml
```

Run the checks and tests:

```powershell
python -m ruff check drone-dispatcher
python -m ruff format --check drone-dispatcher
python -m pytest drone-dispatcher/tests
```
