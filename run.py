# NOTE :
# This is a DEV-ONLY script to run the app locally.
# In production, use a WSGI server like Gunicorn or uWSGI. (obviously)

# run.py

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
