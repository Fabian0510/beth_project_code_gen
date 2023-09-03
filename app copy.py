from flask import Flask, request, send_from_directory, redirect, url_for, flash
import os
import yaml
import csv
import random
from datetime import datetime, timedelta
from faker import Faker
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'yaml', 'yml'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            generate_csv_from_yaml(filepath)

            csv_filename = os.path.splitext(filename)[0] + '.csv'
            return redirect(url_for('download_file', filename=csv_filename))
            
    return '''
    <!doctype html>
    <title>Upload YAML</title>
    <h1>Upload YAML to generate CSV</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


def generate_random_data(data_type):
    if data_type == "int":
        return random.randint(1, 1000)
    elif data_type == "string":
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=10))
    elif data_type == "date":
        start_date = datetime(2000, 1, 1)
        end_date = datetime(2023, 1, 1)
        random_date = start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds())))
        return random_date.strftime('%Y-%m-%d')
    elif data_type == "float":
        return round(random.uniform(1, 1000), 2)
    else:
        return None

def generate_csv_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

    for csv_info in data['csvs']:
        with open(csv_info['name'], 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            headers = [col['name'] for col in csv_info['columns']]
            writer.writerow(headers)
            
            for _ in range(csv_info['rows']):
                row = [generate_random_data(col['type']) for col in csv_info['columns']]
                writer.writerow(row)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)