from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def idx():
    return render_template('index.html')

@app.route('/assessment')
def assessment():
    return render_template('assessment.html')

@app.route('/assessmentold')
def assessmentold():
    return render_template('assessmentold.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/automated-transcription')
def automated_transcription():
    return render_template('automated-transcription.html')

@app.route('/sockettest')
def sockettest():
    return render_template('sockettest_new.html')

@app.route('/create-study')
def create_study():
    return render_template('create-study.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/voice-agent')
def voice_agent():
    return render_template('vapi.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/postresearch')
def postresearch():
    return render_template('post-research-interview.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/sign-up')
def signup():
    return render_template('sign-up.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)