# Space portal

Install all requirements

```bash
sudo apt-get install libpq-dev # if it's a ubuntu vm
pip install -r requirements.txt
```

Deploy

```bash
# Set up the database
python3 manage.py makemigrations
python3 manage.py migrate

# Collect static files
python3 manage.py collectstatic

# Start the application (development mode)
python3 manage.py runserver # default port 8000

# Use in AWS to start the application (run in backgroun)
nohup python3 manage.py runserver 0.0.0.0:8000
```