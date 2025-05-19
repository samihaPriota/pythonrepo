import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
print(type(app))
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def parse_file(filepath):
    records = []
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split('~')
            record = {"type": parts[0]}
            for part in parts[1:]:
                if part[:2].isdigit():
                    record[f"col_{part[:2]}"] = part[2:]
            records.append(record)
    return records

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    return "File uploaded successfully", 200




@app.route('/view/<filename>')
def view_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return "File not found", 404
    records = parse_file(filepath)
    return render_template('table.html', filename=filename, records=records)



@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

@app.route('/records/<filename>', methods=['GET'])
def get_records(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    return jsonify(parse_file(filepath))




if __name__ == '__main__':
    app.run(debug=True)
