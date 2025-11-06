# 1) Create venv (optional)
python -m venv .myenv && source .myenv/bin/activate.bat  # Windows: .myenv\Scripts\activate.bat

# 2) Install
pip install requirements.txt

# 3) Migrate & run
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

# Register
curl -X POST http://127.0.0.1:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"123456"}'

# Login
curl -X POST http://127.0.0.1:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"identifier":"john","password":"123456"}'

