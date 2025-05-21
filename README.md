# 🔧 Federated Learning Clinical Safety Server SDK

This is the documentation for the Federated Learning Clinical Safety Dashboard SDK! This project provides a package for interacting with the [Federated Learning Clinical Safety Dashboard Server](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-server) in a type-safe and easy manner.


[![CI](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-sdk/actions/workflows/ci.yml)

[![SDK ↔ Server Integration](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-sdk/actions/workflows/integration.yml/badge.svg)](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-sdk/actions/workflows/integration.yml)

## Prerequisites

Before you begin, ensure you have the following installed:

* Python 3.10+
* Poetry

### Installing poetry

Windows NT
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Then add to path:

```
%USERPROFILE%\AppData\Roaming\pypoetry\venv\Scripts
```

Linux/MacOS/Unix-like systems:
```bash
pipx install poetry
```

