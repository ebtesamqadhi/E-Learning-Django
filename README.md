# E-Learning-Platform

**Steps to Clone and Run the Project**

1. Clone the repository:
git clone https://github.com/ebtesamqadhi/E-Learning-Platform.git
cd E-Learning-Platform

2. Create and activate a virtual environment:
   
```bash
python -m venv venv
venv\Scripts\activate       # On Windows
or
source venv/bin/activate    # On Linux/Mac
```

4. Install the required packages:

```bash
pip install -r requirements.txt
````
5. Apply database migrations:

````bash
python manage.py migrate
````

6. Create a superuser to access the admin panel (Optional):

````bash
python manage.py createsuperuser
````

7. Run the development server

````bash
python manage.py runserver
````
