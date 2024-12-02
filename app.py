import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_socketio import SocketIO
from flask_migrate import Migrate
from extensions import db
from supabase import create_client, Client
import pathlib

# Load environment variables
print("Loading .env file...")
load_dotenv(find_dotenv())

# Print all environment variables for debugging
print("\nAll environment variables:")
for key, value in os.environ.items():
    if key in ['SUPABASE_URL', 'SUPABASE_KEY', 'FLASK_APP', 'FLASK_ENV', 'DATABASE_URL']:
        masked_value = '***masked***' if 'KEY' in key else value
        print(f"{key}={masked_value}")

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize Supabase client
try:
    # Read environment variables
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    print(f"\nDebug Info:")
    print(f"Raw SUPABASE_URL: {supabase_url}")
    
    # Clean up the URL if needed
    if supabase_url:
        supabase_url = supabase_url.strip().strip("'").strip('"')
    if supabase_key:
        supabase_key = supabase_key.strip().strip("'").strip('"')
    
    print(f"Cleaned SUPABASE_URL: {supabase_url}")
    print(f"SUPABASE_KEY present: {'Yes' if supabase_key else 'No'}")
    
    if not supabase_url or not supabase_key:
        raise ValueError("Missing Supabase credentials")
        
    if not supabase_url.startswith('https://'):
        raise ValueError(f"Invalid Supabase URL format. URL must start with https:// but got: {supabase_url}")
    
    print("Creating Supabase client...")
    supabase: Client = create_client(
        supabase_url=supabase_url,
        supabase_key=supabase_key
    )
    print("Supabase client created successfully!")
    
except Exception as e:
    print(f"Error setting up Supabase: {str(e)}")
    raise

# Add Supabase instance to Flask app config
app.config['supabase'] = supabase
app.config['SUPABASE_URL'] = supabase_url
app.config['SUPABASE_API_KEY'] = supabase_key

# Initialize existing services
db.init_app(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)

from models import Transcription, Assessment, Project
from routes import init_routes

init_routes(app, socketio)

# Helper function to get Supabase client
def get_supabase():
    return app.config['supabase']

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, host='0.0.0.0', port=5000)