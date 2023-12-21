# Space portal

Install all requirements
```bash
pip install -r requirements.txt
```

Deploy
```bash
# Set up the database
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Start the application (development mode)
python manage.py runserver # default port 8000

# Use in AWS to start the application (run in backgroun)
nohup python3 manage.py runserver 0.0.0.0:8000
```