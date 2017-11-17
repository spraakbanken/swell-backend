

Create python 3 virtual environment:
python3 -m venv venv

Activate virtualenv:
source venv/bin/activate

Upgrade pip (sometimes necessary) and install requirements:
pip install --upgrade pip
pip install -r requirements.txt

Run web API:
PATH_TO_BACKEND/app/venv/bin/gunicorn -b 0.0.0.0:55000 index --chdir PATH_TO_BACKEND/app
