from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from tinydb import TinyDB, Query
import os

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize TinyDB database
db = TinyDB('database.json')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Store file path in TinyDB
        db.insert({'filename': filename, 'filepath': file_path})
        
        return redirect(url_for('uploaded_file', filename=filename))
    else:
        return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_entry = db.search(Query().filename == filename)
    if not file_entry:
        return 'File not found!'
    else:
        return render_template('uploaded.html', filepath=file_entry[0]['filepath'])

if __name__ == '__main__':
    app.run(debug=True)
