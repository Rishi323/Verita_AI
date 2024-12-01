import os
from flask import Flask
from flask_socketio import SocketIO
from flask_migrate import Migrate
from extensions import db
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize Supabase client
supabase: Client = create_client(
    supabase_url=os.environ.get('SUPABASE_URL'),
    supabase_key=os.environ.get('SUPABASE_API_KEY')  
)

# Add Supabase instance to Flask app config
app.config['supabase'] = supabase

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
    socketio.run(app, host='0.0.0.0', port=5000)\
    