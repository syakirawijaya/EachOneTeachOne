from flask import Flask, render_template, request, session
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

# The default folder name for static files should be "static"
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'EachOneTeachOne'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=("POST", "GET")) # This is a decorator that registers a function to be called when the root URL / is accessed. It renders the index.html template.
def upload_file(): #  When a file is uploaded via a POST request, it saves the file to the specified upload folder, stores the file path in the Flask session, and renders the uploaded_image.html template.
    if request.method == 'POST':
        uploaded_img = request.files['uploaded-file']
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)

        return render_template('uploaded_image.html')

@app.route('/show_image') # retrieves the uploaded image file path from the Flask session and renders the show_image.html template, passing the file path as a variable to display the image.
def display_image():
    # Retrieving uploaded file
    img_file_path = session.get('uploaded_img_file_path', None)
    # Display image in Flask application web page
    return render_template('show_image.html', user_image=img_file_path)

if __name__ == '__main__':
    app.run(debug=True)