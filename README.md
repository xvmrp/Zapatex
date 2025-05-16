python -m venv venv

IMPORTANTE:

pip install -r requirements.txt
pip install flask
pip install flask requests


.\venv\Scripts\Activate.ps1
----

Comando para iniciarlo:
python app.py




$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
flask run
