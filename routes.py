from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_socketio import emit
from extensions import db
from models import Transcription, Assessment, Project
from fine_tuning import prepare_dataset, fine_tune_model
from grading_framework import grade_transcription, UX_FRAMEWORKS
from sqlalchemy.sql import func
import logging
import traceback
import os
import base64
import dotenv
from openai import OpenAI
from flask import Flask, request, jsonify, render_template
from datetime import datetime

IMAGE_PARSE_PROMPT = """
You are given different images to digest along with a discussion guide and additional context. Your role is to act as an expert user researcher who is extremely knowledgeable in the world of enterprise software.

Discussion Guide Context: {discussion_guide}

Additional Context: {additional_info}

Your questions should be open-ended, probing, and adaptable to the product's evolving features, while following the structure and objectives outlined in the discussion guide. Your goal is to understand the user's perspective and identify opportunities for enhancing the product's usability and user experience.

Consider:
1. Questions from the discussion guide
2. User's workflow and emotional response
3. Potential frustrations or limitations
4. Specific areas of focus mentioned in the guide

Output Format:
#####
General Questions: [1-5 questions aligned with discussion guide]
#####
Image 1: 
[Description of the image]
[(1-3 questions incorporating guide themes)]
###
Image 2: 
[Description of the image]
[(1-3 questions incorporating guide themes)]
###
...
###
Image N: 
[Description of the image]
[(1-3 questions incorporating guide themes)]
#####
"""

INTERVIEW_PROMPT = """
You are an experienced UI/UX interviewer. You are tasked with interviewing a user about their experience with the product shown in the images. There are questions already prepared for you to ask below.
Refer to each image by its number. Wait for a user response before moving on to the next question. Feel free to ask follow-up questions to get more insights based on the image descriptions.
Space out the general questions throughout the interview, DO NOT ask them all at the beginning. Ask at most one general question at the beginning. There may be contexts where a general question is a suitable follow-up to a user's response.
"""

dotenv.load_dotenv()
client = OpenAI()
client.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

def get_openai_response(imageList, additionalInfo, guide_content=None):
    # Format the prompt with discussion guide and additional info
    formatted_prompt = IMAGE_PARSE_PROMPT.format(
        discussion_guide=guide_content if guide_content else "No discussion guide provided.",
        additional_info=additionalInfo if additionalInfo else "No additional context provided."
    )
    
    # Log the final formatted prompt
    logger.info("Final formatted prompt with discussion guide:")
    logger.info(formatted_prompt)
    
    content_partial = [{"type": "image_url", "image_url":{"url": image}} for image in imageList]
    content_partial.append({"type": "text", "text": formatted_prompt})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": content_partial
            }
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
    )
    return response.choices[0].message.content

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_routes(app, socketio):
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
    
    @app.route('/automated-transcription')
    def automated_transcription():
        return render_template('automated-transcription.html')
    
    @app.route('/create-study', methods=['GET'])
    def create_study():
        return render_template('create-study.html')
    
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

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/api/chat', methods=['POST'])
    def chat():
        # Parse form data into JSON
        p_json = request.form.to_dict(flat=False)
        imageList = request.files
        additionalInfo = p_json.get('additionalInfo')[0] if p_json.get('additionalInfo') else ""
        additionalQuestions = p_json.get('additionalQuestions')[0] if p_json.get('additionalQuestions') else ""
        
        if not imageList:
            return jsonify({'error': 'Images are required'}), 400
        
        # Handle discussion guide file
        guide_file = request.files.get('guide')
        guide_content = None
        if guide_file:
            try:
                logger.info(f"Processing discussion guide file: {guide_file.filename}")
                # Read and process the discussion guide based on file type
                if guide_file.filename.endswith('.txt'):
                    guide_content = guide_file.read().decode('utf-8')
                    logger.info("TXT Content extracted:")
                    logger.info(guide_content)
                elif guide_file.filename.endswith('.pdf'):
                    from PyPDF2 import PdfReader
                    reader = PdfReader(guide_file)
                    guide_content = "\n".join([page.extract_text() for page in reader.pages])
                    logger.info("PDF Content extracted:")
                    logger.info(guide_content)
                elif guide_file.filename.endswith(('.doc', '.docx')):
                    from docx import Document
                    doc = Document(guide_file)
                    guide_content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                    logger.info("DOCX Content extracted:")
                    logger.info(guide_content)
                logger.info("Successfully processed discussion guide file")
            except Exception as e:
                logger.error(f"Error processing discussion guide file: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                return jsonify({'error': 'Failed to process discussion guide file'}), 400
        else:
            logger.info("No discussion guide file provided")
        
        # Reformat image data to be compatible with OpenAI API
        try:
            imageList = [
                f"data:{image.content_type};base64,{base64.b64encode(image.read()).decode('utf-8')}"
                for image in imageList.getlist('images')
            ]
        except Exception as e:
            logger.error(f"Error processing image files: {str(e)}")
            return jsonify({'error': 'Failed to process image files'}), 400

        try:
            response = get_openai_response(imageList, additionalInfo, guide_content)

            if additionalQuestions:
                response += f"\n{additionalQuestions}"

            vapi_override_message = {
                'firstMessage': "Welcome to this interview! I'd love to ask you some questions based on the discussion guide and images provided.",
                'model': {
                    'provider': "openai",
                    'model': "gpt-3.5-turbo",
                    'messages': [
                        {
                            'role': "system",
                            'content': INTERVIEW_PROMPT,
                        },
                        {
                            'role': "system",
                            'content': response,
                        },
                    ],
                },
            }

            return jsonify({'response': vapi_override_message})
        except Exception as e:
            logger.error(f"Error in chat processing: {str(e)}")
            return jsonify({'error': 'An error occurred while processing your request'}), 500

    @app.route('/voice-agent')
    def voice_agent():
        return render_template('vapi.html')
    
    @app.route('/pricing')
    def pricing():
        return render_template('pricing.html')

    @app.route('/resources')
    def resources():
        return render_template('resources.html')
    
    @app.route('/postresearch')
    def postresearch():
        return render_template('post-research-interview.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            try:
                data = request.get_json()
                email = data.get('email')
                password = data.get('password')

                if not all([email, password]):
                    return jsonify({'error': 'Missing email or password'}), 400

                # Get Supabase client from app config
                supabase = app.config['supabase']
                
                # Sign in user with Supabase
                auth_response = supabase.auth.sign_in_with_password({
                    'email': email,
                    'password': password
                })

                if not auth_response or not auth_response.user:
                    return jsonify({'error': 'Invalid credentials'}), 401

                # Get user profile
                profile_response = supabase.from_('user_profiles').select('*').eq('id', auth_response.user.id).execute()
                
                if hasattr(profile_response, 'error') and profile_response.error:
                    logger.error(f"Profile fetch error: {profile_response.error}")
                    return jsonify({'error': 'Failed to fetch user profile'}), 400

                user_profile = profile_response.data[0] if profile_response.data else None

                return jsonify({
                    'success': True,
                    'user': {
                        'id': auth_response.user.id,
                        'email': auth_response.user.email,
                        'type': user_profile.get('user_type') if user_profile else None
                    }
                }), 200

            except Exception as e:
                logger.error(f"Login error: {str(e)}")
                return jsonify({'error': 'An unexpected error occurred'}), 500

        # GET request - render the login template
        return render_template('login.html')

    @app.route('/sign-up', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            try:
                data = request.get_json()
                name = data.get('name')
                email = data.get('email')
                password = data.get('password')
                user_type = data.get('userType')

                if not all([name, email, password, user_type]):
                    return jsonify({'error': 'Missing required fields'}), 400

                # Get Supabase client from app config
                supabase = app.config['supabase']
                
                # Sign up user with Supabase
                auth_response = supabase.auth.sign_up({
                    'email': email,
                    'password': password,
                    'data': {
                        'full_name': name
                    }
                })

                if not auth_response or not auth_response.user:
                    return jsonify({'error': 'No user data returned from sign up'}), 400

                try:
                    # Create user profile with user type
                    profile_response = supabase.rpc(
                        'create_user_profile',
                        {
                            'user_id': auth_response.user.id,
                            'user_full_name': name,
                            'user_email': email,
                            'user_type': user_type
                        }
                    ).execute()

                    if hasattr(profile_response, 'error') and profile_response.error:
                        logger.error(f"Profile creation error: {profile_response.error}")
                        # If profile creation fails, we should clean up the auth user
                        supabase.auth.admin.delete_user(auth_response.user.id)
                        return jsonify({'error': 'Failed to create user profile'}), 400

                except Exception as profile_error:
                    logger.error(f"Profile creation error: {str(profile_error)}")
                    # Clean up auth user if profile creation fails
                    supabase.auth.admin.delete_user(auth_response.user.id)
                    return jsonify({'error': 'Failed to create user profile'}), 400

                return jsonify({
                    'success': True, 
                    'user': {
                        'id': auth_response.user.id,
                        'email': auth_response.user.email,
                        'type': user_type
                    }
                }), 200

            except Exception as e:
                logger.error(f"Sign-up error: {str(e)}")
                return jsonify({'error': 'An unexpected error occurred'}), 500

        # GET request - render the sign-up template
        return render_template('sign-up.html')

    @app.route('/ab-testing')
    def usabilitytest():
        return render_template('ab-testing.html')

    @app.route('/onboarding/user-type')
    def onboarding_user_type():
        return render_template('onboarding/user-type.html')

    @app.route('/onboarding/experience-level')
    def onboarding_experience_level():
        return render_template('onboarding/experience-level.html')

    @app.route('/onboarding/goals')
    def onboarding_goals():
        return render_template('onboarding/goals.html')

    @app.route('/onboarding/complete')
    def onboarding_complete():
        return render_template('onboarding/complete.html')

# ... rest of the code remains the same ...
