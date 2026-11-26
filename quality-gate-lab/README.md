# Cashback quality gate

Install the development tools and enable the repository's pre-commit hooks:

```powershell
python -m pip install -r quality-gate-lab/requirements-dev.txt
pre-commit install
```

Run the checks manually:

```powershell
pre-commit run --all-files
```

The hooks lint and format Python files in this lab, then run its pytest suite.
