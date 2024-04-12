# Import necessary modules from Flask and Werkzeug
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os

# Create a Flask application instance
app = Flask(__name__)

# Define the upload folder where uploaded files will be stored
UPLOAD_FOLDER = 'static/uploads/'

# Set the secret key for the application
app.secret_key = "secret key"

# Configure the upload folder and set maximum content length for file uploads
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB maximum file size

# Ensure the upload folder exists. If not, create it.
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Set the allowed file extensions for file uploads
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Function to check if the filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
# Define route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define route for uploading images via POST request
@app.route('/', methods=['POST'])
def upload_image():
    # Check if the request contains a file
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # Check if no file was selected
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    # Check if the uploaded file has an allowed extension
    if file and allowed_file(file.filename):
        # Secure the filename to prevent malicious file uploads
        filename = secure_filename(file.filename)
        # Save the uploaded file to the upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Flash a success message
        flash('Image successfully uploaded and displayed below')
        # Render the home page template with the uploaded image displayed
        return render_template('index.html', filename=filename)
    else:
        # Flash a message indicating that only certain image types are allowed
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

# Define route for displaying the uploaded image
@app.route('/display/<filename>')
def display_image(filename):
    # Redirect to the URL of the uploaded image
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

# Run the Flask application if this script is executed directly
if __name__ == "__main__":
    app.run()
