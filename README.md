# E-Learning-Platform

**Steps to Clone and Run the Project**

1. Clone the repository:

```bash
git clone https://github.com/ebtesamqadhi/E-Learning-Platform.git
cd E-Learning-Platform
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows
```bash
venv\Scripts\activate
```

On Linux/Mac
```bash
source venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```
4. Apply database migrations:

```bash
python manage.py migrate
```

5. Create a superuser to access the admin panel (Optional):

```bash
python manage.py createsuperuser
```

6. Run the development server

```bash
python manage.py runserver
```
