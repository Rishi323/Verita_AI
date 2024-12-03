# app.py
import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_migrate import Migrate
from extensions import db
from supabase import create_client
import pathlib

# Load environment variables
print("Loading .env file...")
load_dotenv(find_dotenv())

# Print selected environment variables for debugging (masked where sensitive)
print("\nAll environment variables:")
for key, value in os.environ.items():
    if key in ['SUPABASE_URL', 'SUPABASE_SERVICE_ROLE_KEY', 'FLASK_APP', 'FLASK_ENV', 'DATABASE_URL']:
        masked_value = '***masked***' if 'KEY' in key else value
        print(f"{key}={masked_value}")

# Flask application setup
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "a secret key")
database_url = os.environ.get("DATABASE_URL")

# Ensure the database URL is compatible with SQLAlchemy
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize Supabase client
try:
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

    if not supabase_url or not supabase_key:
        raise ValueError("Missing Supabase credentials")

    # Clean and validate the Supabase URL
    supabase_url = supabase_url.strip().strip("'").strip('"')
    if not supabase_url.startswith('https://'):
        raise ValueError(f"Invalid Supabase URL format. Must start with https:// but got: {supabase_url}")

    # Create the Supabase client
    supabase = create_client(supabase_url, supabase_key)
    app.config['supabase'] = supabase
    print("Supabase client initialized successfully!")

except Exception as e:
    print(f"Error initializing Supabase client: {str(e)}")
    supabase = None

# Add Supabase-related configurations
app.config['SUPABASE_URL'] = supabase_url
app.config['SUPABASE_API_KEY'] = supabase_key

# Initialize Flask extensions
db.init_app(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)

# Import models and routes
from models import Transcription, Assessment, Project
from routes import init_routes

# Initialize application routes
init_routes(app, socketio)

# Additional routes
@app.route('/ab-testing')
def ab_testing():
    return render_template('ab-testing.html')

# Helper function for accessing Supabase client
def get_supabase():
    return app.config.get('supabase')

# Main application entry point
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Explicitly set optional arguments for run method
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=True, log_output=True)
