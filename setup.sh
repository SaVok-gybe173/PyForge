#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PY_VERSION="python3"

# Обработка аргументов: -v <версия> или -v без версии
if [ "$1" = "-v" ]; then
    if [ -n "$2" ]; then
        PY_VERSION="python$2"
    else
        PY_VERSION="python"
    fi
fi

cd _core/creating/progress
$PY_VERSION setup.py build_ext --inplace

cd "$SCRIPT_DIR"
cd _core/creating/listing
$PY_VERSION setup.py build_ext --inplace

cd "$SCRIPT_DIR"
cd _core/game3D
$PY_VERSION setup.py build_ext --inplace