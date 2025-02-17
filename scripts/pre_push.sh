set -e
pip install black isort pylint
# get folder path of this script

SCRIPT_FILE_PATH=$(readlink -f ${BASH_SOURCE[0]})
SCRIPT_FOLDER_PATH=$(dirname ${SCRIPT_FILE_PATH})

pushd "${SCRIPT_FOLDER_PATH}/../" > /dev/null
echo "Running pre-push hook"
black . --check
isort . --check-only
echo "$PWD"
PYTHONPATH=. pylint pyllm --rcfile .pylintrc

ENV=development python -m pytest -s

exit 0
