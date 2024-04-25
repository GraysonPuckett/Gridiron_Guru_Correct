# app.py
import os
from app import create_app

# Set the secret key. Remember, in a real application, use a more secure method
# Ideally, load this from an environment variable or a config file
app.secret_key = '12345'

# Initialize the Flask application using the application factory
app = create_app()



if __name__ == '__main__':
    app.run(debug=True)
