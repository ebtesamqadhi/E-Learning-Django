# E-Learning-Platform

**Steps to Clone and Run the Project**

1. Clone the repository:
git clone https://github.com/ebtesamqadhi/E-Learning-Platform.git
cd E-Learning-Platform

2. Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate       # On Windows
or
source venv/bin/activate    # On Linux/Mac

3. Install the required packages:
pip install -r requirements.txt

4. Apply database migrations:
python manage.py migrate

5. Create a superuser to access the admin panel (Optional):
python manage.py createsuperuser

6. Run the development server
python manage.py runserver

