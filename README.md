# VFD Clippy Host
Host MacOS service for VFD Clippy

## Quick Installation Setup
1. `cd scripts`
1. `./install.sh`

## Developer Setup
### Initialize environment
1. `python3 -m venv venv`
1. `source venv/bin/activate`
1. `pip install -r requirements.txt`
1. `pip install -r requirements-dev.txt`

### Modify and Build Executable
1. Modify project files if desired
1. `cd scripts`
1. `./build_exec.sh`
1. `./install.sh`

## Uninstall
1. `cd scripts`
1. `./uninstall.sh`