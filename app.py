from flask import Flask, request, jsonify, render_template, url_for
from PIL import Image
import os
import shutil
import webbrowser
import threading
import subprocess
from modules.pp import new_pp
from modules import mcq_funcs, pp_funcs, uuids
import json

from modules.snippets import snippets

# Configuration settings
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Main Routes
@app.route('/')
def home():
    return render_template('base.html')

@app.route('/practice-problem-generator', methods=['GET'])
def practice_problem_generator():
    return render_template('practice-problem-generator.html')

@app.route('/multiple-choice-generator', methods=['GET'])
def multiple_choice_generator():
    return render_template('multiple-choice-generator.html')

@app.route('/uuid-replacer', methods=['GET'])
def uuid_replacer():
    return render_template('uuid-replacer.html')

@app.route('/code-snippet', methods=['GET'])
def code_snippet():
    return render_template('code-snippet.html')

@app.route('/pygments', methods=['GET'])
def pygments():
    return render_template('pygments.html')

@app.route('/pick-code', methods=['GET'])
def pick_code():
    return render_template('pick-code.html')

# Helper Routes
@app.route('/open_save_dir', methods=['GET'])
def open_save_dir():
    # Open the save directory
    subprocess.run(['open', '-a', 'Finder', 'output/.'])
    return jsonify(), 200

# Practice Problem Generator routes
@app.route('/practice-problem-generator/parse-gif', methods=['POST'])
def parse_gif():
    try:
        return jsonify(pp_funcs.parse_gif(request.files['gif'])), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/save_card', methods=['POST'])
def save_card():
    try:
        pp_funcs.save_card(
            int(request.form['num_mcqs']),
            request.form['filename'],
            request.form['projectname'],
            request.files['card'],
        )
        return jsonify(), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/replace_uuids', methods=['POST'])
def replace_uuids():
    file = request.files['file']
    from modules.uuids import process_file
    process_file(file)
    open_save_dir()
    return jsonify(), 200

## Multiple Choice Generator routes
@app.route('/multiple-choice-generator/mcq', methods=['POST'])
def new_mcq():
    try:
        data = mcq_funcs.new_mcq(int(request.form['number-of-questions']))
        return json.dumps(data), 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/multiple-choice-generator/exam', methods=['POST'])
def new_exam():
    try:
        data = mcq_funcs.new_exam(int(request.form['number-of-questions']))
        return json.dumps(data), 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
## UUID Replacer routes
@app.route('/uuid-replacer/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        from modules.uuids import process_file
        process_file(file)
        open_save_dir()
        return jsonify(), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
## Code Snippet routes
@app.route('/highlight', methods=['POST'])
def highlight_code():

    # Parse the JSON strings back to lists of integers if they are not empty or null
    # mark_starts = json.loads(request.form.get('markStarts')) if request.form.get('markStarts') else []
    # mark_ends = json.loads(request.form.get('markEnds')) if request.form.get('markEnds') else []
    # strike_starts = json.loads(request.form.get('strikeStarts')) if request.form.get('strikeStarts') else []
    # strike_ends = json.loads(request.form.get('strikeEnds')) if request.form.get('strikeEnds') else []

    return jsonify({"highlighted_code":snippets.highlight_code(
        request.form.get('code'), request.form.get('language')
    )}), 200

@app.route('/get_styles', methods=['POST'])
def get_styles():
    return jsonify({"styles":snippets.get_styles(
        request.form.get('language')
    )}), 200


## App start-up

def open_browser():
    # Wait for a moment to ensure the Flask app has started
    import time
    time.sleep(2)  # Adjust the sleep duration as needed

    # Open a web browser to the specified URL (e.g., http://localhost:5000)
    url = 'http://127.0.0.1:5000'  # Change the port number as needed
    webbrowser.open(url)

# Entry point
def start_app():
    # Create a thread to open the web browser
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.start()

    # Start the Flask app in the main thread
    app.run(debug=True)


# Allows for running the app from the command line
if __name__ == '__main__':
    # Start the Flask app in the main thread
    # app.run(debug=True)
    #OR!!! Start with auto-open browser
    start_app()