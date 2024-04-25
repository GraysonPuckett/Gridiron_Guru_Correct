# app.py
import os
from app import create_app


# Initialize the Flask application using the application factory
app = create_app()

# Set the secret key. Remember, in a real application, use a more secure method
# Ideally, load this from an environment variable or a config file
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', '12345')

if __name__ == '__main__':
    app.run(debug=True)
