#!/usr/bin/bash

CUR_PATH="$PWD"
REL_TO_HOME="${CUR_PATH/#$HOME\//}"
PROJ_DIR="${REL_TO_HOME%%/*}"

echo "${HOME}/${PROJ_DIR}/scripts/deploysection.py"
python3 "${HOME}/${PROJ_DIR}/scripts/deploysection.py" "$@"
