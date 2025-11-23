import os
from flask import Flask, render_template, request, send_file, flash, redirect, url_for, after_this_request
from werkzeug.utils import secure_filename
from utils.converters import convert_file

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this for production

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'webp', 'csv', 'json', 'xlsx', 'xls', 'yaml', 'yml', 'md'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        conversion_type = request.form.get('conversion_type')
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            output_path_full = None
            try:
                output_filename = convert_file(filepath, conversion_type, app.config['DOWNLOAD_FOLDER'])
                output_path_full = os.path.join(app.config['DOWNLOAD_FOLDER'], output_filename)
                
                # Schedule file deletion after request
                @after_this_request
                def remove_files(response):
                    try:
                        if os.path.exists(filepath):
                            os.remove(filepath)
                        if output_path_full and os.path.exists(output_path_full):
                            os.remove(output_path_full)
                    except Exception as error:
                        app.logger.error("Error removing or closing downloaded file handle", error)
                    return response

                return send_file(output_path_full, as_attachment=True)
            except Exception as e:
                # If something goes wrong, try to clean up the uploaded file
                if os.path.exists(filepath):
                    os.remove(filepath)
                flash(str(e))
                return redirect(request.url)
        else:
            flash('File type not allowed')
            return redirect(request.url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
