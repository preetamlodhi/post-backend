# BackendAssignment

Project for the api App to enable User registration, User login and Post creation.

# Deployment Instructions

1. Install python3.8
    - `sudo apt-get update`
    - `sudo apt-get install python3.8`
1. Install pip for python3
    - `sudo apt-get update`
    - `sudo apt-get  install python3-pip`
1. Install git
    - `sudo apt-get install git-core`
1. Install virtual environment
    - `sudo apt-get install python3-venv`
1. Clone the project from git
1. cd to the project root folder _BackendAssignment_
1. Create a virtual environment _envapi_
    - `python3 -m venv envapi`
1. Activate the above virtual environment
    - `source envapi/bin/activate`
1. Install dependencies from _requirements.txt_ file 
    - `pip install -r requirements.txt`
1. Create Migrations 
    - `python manage.py makemigrations`
1. Apply Migrations
    - `python manage.py migrate`
1. Run the test server
    - `python3 manage.py runserver`
1. The File `api.postman_collection.json` has Postman Collection  which can be imported in postman to test the apis.

