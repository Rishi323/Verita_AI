import os
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_migrate import Migrate
from extensions import db, init_extensions
from routes import init_routes

def create_app():
    app = Flask(__name__)
    
    # Configure your database URL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///verita.db'  # for SQLite
    # or
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'  # for PostgreSQL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    init_extensions(app)
    
    # Initialize SocketIO
    socketio = SocketIO(app)
    
    # Initialize routes
    init_routes(app, socketio)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
    
    return app, socketio

from models import Transcription, Assessment, Project
app, socketio = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)
