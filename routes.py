from flask import render_template, request, redirect, url_for, flash
from extensions import db
from models import Transcription, Assessment
from fine_tuning import prepare_dataset, fine_tune_model
from grading_framework import grade_transcription

def init_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            transcription_text = request.form['transcription']
            new_transcription = Transcription(text=transcription_text)
            db.session.add(new_transcription)
            db.session.commit()

            assessment_result = grade_transcription(transcription_text)
            new_assessment = Assessment(transcription_id=new_transcription.id, result=assessment_result)
            db.session.add(new_assessment)
            db.session.commit()

            return redirect(url_for('results', transcription_id=new_transcription.id))

        return render_template('index.html')

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
