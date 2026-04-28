# Interview Tracker Project Setup
# This project helps prepare interview questions and maintain summaries of attended interviews.

# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Create migrations
python manage.py makemigrations
python manage.py makemigrations "interviews"

# Step 3: Apply migrations
python manage.py migrate

# Step 4: Run the development server
python manage.py runserver --settings=interviewTracker.settings

# Optional:
# Run the server with a custom port or environment settings:
# python manage.py runserver 7000 --settings=interviewTracker.prod_settings
# python manage.py runserver --settings=interviewTracker.staging_settings
