# accredited to https://github.com/haoxuw/ato/blob/master/ato_mesh/scripts/setup_venv.sh

VENV_FOLDER_NAME='venv'

SCRIPT_FILE_PATH=$(readlink -f ${BASH_SOURCE[0]})
SCRIPT_FOLDER_PATH=$(dirname ${SCRIPT_FILE_PATH})

pushd "${SCRIPT_FOLDER_PATH}/../" > /dev/null

[ ! -d "${VENV_FOLDER_NAME}" ] && echo "Creating python virtual environment under ${VENV_FOLDER_NAME}" && python -m venv ${VENV_FOLDER_NAME}

source ${VENV_FOLDER_NAME}/bin/activate
echo "Creating virtual environment, the initial run might take a while..."
pip install --upgrade pip && pip install -r ./requirements.txt

if [ $? -ne 0 ]; then
    echo "Failed to install dependencies, please check the error message and try again."
    exit 1
fi
popd > /dev/null

echo
echo "Virtual environment activated @ ${SCRIPT_FOLDER_PATH}/../${VENV_FOLDER_NAME}"
echo