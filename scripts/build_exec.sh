#!/bin/bash
set -e

rm -rf ../dist/*

echo "Building vfd-clippy..."
pyinstaller \
  --onefile \
  --name vfd-clippy \
  --distpath ../dist \
  --workpath ../build \
  --specpath ../ \
  ../src/vfd_clippy.py


echo "✅ Build complete. Executable is ../dist/vfd-clippy"