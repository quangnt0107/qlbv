# qlbv

mac/ubuntu
cmd
python -m venv env
source env/bin/active

export FLASK_APP=run.py
export FLASK_ENV=development

pip install -r requirements.txt  

flask run


window
cmd
python -m env env
./venv/Scripts/activate

set FLASK_APP=run.py
set FLASK_ENV=development

pip install -r requirements.txt  


flask run
