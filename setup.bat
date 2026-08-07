@echo off
cd /d "%~dp0"

set PY_VERSION=python
if "%1"=="-v" set PY_VERSION=py -%2
if "%1"=="-v" if "%2"=="" set PY_VERSION=python

cd _core\creating\progress
%PY_VERSION% setup.py build_ext --inplace

cd /d "%~dp0"
cd _core\creating\listing
%PY_VERSION% setup.py build_ext --inplace 

cd /d "%~dp0"
cd _core\game3D
%PY_VERSION% setup.py build_ext --inplace 

cd /d "%~dp0"
cd cpu\game3D
%PY_VERSION% setup.py build_ext --inplace