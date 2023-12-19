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
```