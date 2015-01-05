# shell script that runs the mist monitor pythong script.
# Expects a username and password parameters.
# Usage:
# 	github-pr-scanner.sh <mist_username> <mist_password>

if [ -d git_venv ];
then
    echo "Activating existing virtual env"
    . git_venv/bin/activate
else
    mkdir git_venv
    echo "Creating new virtual env"
    virtualenv git_venv
    . git_venv/bin/activate
fi

pip install github3.py

PATH_TO_SCRIPT=`dirname $0`

python $PATH_TO_SCRIPT/github-open-prs.py $1 $2 $3
