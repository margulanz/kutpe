# kutpe

# Installation

1. `git clone https://github.com/margulanz/kutpe.git`
2. `cd kutpe`
3. `python -m venv venv`
4. `.\venv\scripts\activate`
5. `pip install -r requirements.txt`
6. `python manage.py migrate`
7. `python manage.py createsuperuser`
8. `python manage.py runserver`

# API

- `/get-nearest-banks/` - [POST] request body should be `{"lon":"float","lat":"float"}`
- `/get-nearest-banks-by-location/` - [POST] request body should be `{"location":"name of some location"}`
- `/swagger/`
- `/get-time/` - [POST] request body should be `{"num_servers":int,"inter_arrival_time":int,"max_service":int,"min_service":int}`
