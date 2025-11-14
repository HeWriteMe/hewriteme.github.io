#!/usr/bin/bash

CUR_PATH="$PWD"
REL_TO_HOME="${CUR_PATH/#$HOME\//}"
PROJ_DIR="${REL_TO_HOME%%/*}"

python3 "${HOME}/${PROJ_DIR}/scripts/deployindex.py"


