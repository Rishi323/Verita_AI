from flask import render_template, request, redirect, url_for, flash, jsonify, abort
from flask_socketio import emit, SocketIO
from extensions import db
from models import Transcription, Assessment, Project
from fine_tuning import prepare_dataset, fine_tune_model
from grading_framework import grade_transcription, UX_FRAMEWORKS
from sqlalchemy.sql import func
import logging
import traceback
from services.storage_service import StorageService
from werkzeug.utils import secure_filename

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

storage = StorageService()

def init_routes(app, socketio=None):
    if socketio is None:
        socketio = SocketIO(app)
    
    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route('/assessment', methods=['GET'])
    def assessment():
        return render_template('assessment.html', frameworks=UX_FRAMEWORKS)

    @app.route('/assessmentold', methods=['GET'])
    def assessmentold():
        return render_template('assessmentold.html', frameworks=UX_FRAMEWORKS)

    @app.route('/features', methods=['GET'])
    def features():
        return render_template('features.html')

    @app.route('/fine-tune', methods=['POST'])
    def fine_tune():
        dataset = prepare_dataset()
        model_name = fine_tune_model(dataset)
        flash(f"Model fine-tuned successfully. New model name: {model_name}", 'success')
        return redirect(url_for('index'))

    @socketio.on('transcribe')
    def handle_transcription(data):
        try:
            logger.info(f"Received transcription: {data['transcription']}")
            logger.info(f"Selected framework: {data['framework']}")
            transcription_text = data['transcription']
            framework = data['framework']
            project_id = data.get('project_id')
            
            if not transcription_text:
                raise ValueError("Transcription text is empty")

            new_transcription = Transcription(text=transcription_text, project_id=project_id)
            db.session.add(new_transcription)
            db.session.commit()
            logger.info(f"New transcription created with ID: {new_transcription.id}")

            assessment_result = grade_transcription(transcription_text, framework)
            new_assessment = Assessment(transcription_id=new_transcription.id, result=assessment_result)
            db.session.add(new_assessment)
            db.session.commit()
            logger.info(f"New assessment created for transcription ID: {new_transcription.id}")

            logger.info(f"Emitting assessment result: {assessment_result}")
            emit('assessment_result', {
                'transcription_id': new_transcription.id,
                'assessment': assessment_result
            })
        except Exception as e:
            logger.error(f"Error in handle_transcription: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            db.session.rollback()
            emit('assessment_error', {'error': str(e)})

    @app.route('/get-latest-assessment', methods=['GET'])
    def get_latest_assessment():
        latest_assessment = Assessment.query.order_by(Assessment.id.desc()).first()
        if latest_assessment:
            return jsonify({
                'transcription_id': latest_assessment.transcription_id,
                'assessment': latest_assessment.result
            })
        else:
            return jsonify({'error': 'No assessments available'}), 404

    @app.route('/create-project', methods=['POST'])
    def create_project():
        name = request.form.get('project_name')
        description = request.form.get('project_description')
        if name:
            new_project = Project(name=name, description=description)
            db.session.add(new_project)
            db.session.commit()
            flash('Project created successfully', 'success')
        else:
            flash('Project name is required', 'error')
        return redirect(url_for('dashboard'))

    @app.route('/api/insights')
    def get_insights():
        try:
            avg_insights = db.session.query(
                func.avg(func.jsonb_array_length(Assessment.result['key_insights'])).label('avg_key_insights'),
                func.avg(func.jsonb_array_length(Assessment.result['user_pain_points'])).label('avg_user_pain_points'),
                func.avg(func.jsonb_array_length(Assessment.result['areas_for_improvement'])).label('avg_areas_for_improvement')
            ).first()

            key_findings = db.session.query(
                Assessment.result['key_insights'][0].astext.label('key_insight'),
                Assessment.result['user_pain_points'][0].astext.label('user_pain_point'),
                Assessment.result['areas_for_improvement'][0].astext.label('area_for_improvement')
            ).order_by(func.random()).limit(3).all()

            project_comparison = db.session.query(
                Project.name,
                func.avg(func.jsonb_array_length(Assessment.result['key_insights'])).label('avg_key_insights'),
                func.avg(func.jsonb_array_length(Assessment.result['user_pain_points'])).label('avg_user_pain_points'),
                func.avg(func.jsonb_array_length(Assessment.result['areas_for_improvement'])).label('avg_areas_for_improvement'),
                func.avg(func.cast(func.cast(Assessment.result['overall_quality_score'].astext, db.String), db.Float)).label('avg_quality_score')
            ).join(Transcription, Transcription.project_id == Project.id) \
             .join(Assessment, Assessment.transcription_id == Transcription.id) \
             .group_by(Project.id).all()

            return jsonify({
                'avg_insights': [float(avg_insights.avg_key_insights or 0), float(avg_insights.avg_user_pain_points or 0), float(avg_insights.avg_areas_for_improvement or 0)] if avg_insights else [0, 0, 0],
                'key_findings': [
                    {'key_insight': kf.key_insight, 'user_pain_point': kf.user_pain_point, 'area_for_improvement': kf.area_for_improvement}
                    for kf in key_findings if kf.key_insight and kf.user_pain_point and kf.area_for_improvement
                ],
                'project_comparison': [
                    {
                        'name': project.name,
                        'avg_key_insights': float(project.avg_key_insights or 0),
                        'avg_user_pain_points': float(project.avg_user_pain_points or 0),
                        'avg_areas_for_improvement': float(project.avg_areas_for_improvement or 0),
                        'avg_quality_score': float(project.avg_quality_score or 0)
                    } for project in project_comparison
                ]
            })
        except Exception as e:
            logger.error(f"Error in get_insights: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({'error': 'An error occurred while fetching insights'}), 500

    # New Endpoints:
    @app.route('/studies', methods=['GET'])
    def studies():
        try:
            return render_template('studies.html')
        except TemplateNotFound:
            abort(404)

    @app.route('/studies/create', methods=['POST'])
    def create_studies():
        name = request.form.get('study_name')
        description = request.form.get('study_description')
        if name:
            new_study = Study(name=name, description=description)
            db.session.add(new_study)
            db.session.commit()
            flash('Study created successfully', 'success')
        else:
            flash('Study name is required', 'error')
        return redirect(url_for('dashboard'))

    @app.route('/session/<id>/analyze', methods=['GET'])
    def analyze_session(id):
        session_data = Session.query.get(id)
        if session_data:
            return render_template('analyze_session.html', session_data=session_data)
        else:
            return jsonify({'error': 'Session not found'}), 404

    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'file' not in request.files:
            return 'No file uploaded', 400
        
        file = request.files['file']
        if file.filename == '':
            return 'No file selected', 400
        
        filename = secure_filename(file.filename)
        file_url = storage.save_file(file, filename)
        return {'url': file_url}

    @app.route('/guide-generator')
    def guide_generator():
        return render_template('features/guide_generator.html')

    @app.route('/interview-demo')
    def interview_demo():
        return render_template('features/interview_demo.html')

    @app.route('/analysis-demo')
    def analysis_demo():
        return render_template('features/analysis_demo.html')

    @app.route('/video-demo')
    def video_demo():
        return render_template('features/video_demo.html')

    @app.route('/insights-demo')
    def insights_demo():
        return render_template('features/insights_demo.html')

    @app.route('/dashboard-demo')
    def dashboard_demo():
        return render_template('features/dashboard_demo.html')

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
