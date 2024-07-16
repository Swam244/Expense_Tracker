if ! command -v pip &> /dev/null
then
    echo "pip could not be found. Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py --user
    export PATH=$PATH:~/.local/bin
fi
pip install -r requirements.txt
python3.9 manage.py collectstatic
