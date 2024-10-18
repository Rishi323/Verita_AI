from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_socketio import emit
from extensions import db
from models import Transcription, Assessment
from fine_tuning import prepare_dataset, fine_tune_model
from grading_framework import grade_transcription, UX_FRAMEWORKS

def init_routes(app, socketio):
    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html', frameworks=UX_FRAMEWORKS)

    @app.route('/results/<int:transcription_id>')
    def results(transcription_id):
        transcription = Transcription.query.get_or_404(transcription_id)
        assessment = Assessment.query.filter_by(transcription_id=transcription_id).first()
        return render_template('results.html', transcription=transcription, assessment=assessment)

    @app.route('/fine-tune', methods=['POST'])
    def fine_tune():
        dataset = prepare_dataset()
        model_name = fine_tune_model(dataset)
        flash(f"Model fine-tuned successfully. New model name: {model_name}", 'success')
        return redirect(url_for('index'))

    @socketio.on('transcribe')
    def handle_transcription(data):
        try:
            print(f"Received transcription: {data['transcription']}")
            print(f"Selected framework: {data['framework']}")
            transcription_text = data['transcription']
            framework = data['framework']
            new_transcription = Transcription(text=transcription_text)
            db.session.add(new_transcription)
            db.session.commit()

            assessment_result = grade_transcription(transcription_text, framework)
            new_assessment = Assessment(transcription_id=new_transcription.id, result=assessment_result)
            db.session.add(new_assessment)
            db.session.commit()

            print(f"Emitting assessment result: {assessment_result}")
            emit('assessment_result', {
                'transcription_id': new_transcription.id,
                'assessment': assessment_result
            })
        except Exception as e:
            print(f"Error in handle_transcription: {e}")
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
