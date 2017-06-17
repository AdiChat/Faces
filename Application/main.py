import os
import subprocess
from flask import Flask, request, render_template, url_for, send_from_directory
import compute
import glob
import random

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['upload'] = 'upload'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload/<filename>')
def show(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def front():
    return render_template('front.html')

@app.route('/nobel', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template("home.html", error="sa")
    elif request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            cmd = ['./processing.sh upload/' + file.filename]
            subprocess.call(cmd, shell=True)
            data = glob.glob("data1/eigenfaces/*.png")
            out = compute.compute(data, ['upload/' + file.filename.split('.')[0] + '.png'], 100)
            inputt = url_for('show', filename=file.filename.split('.')[0] + '.png')
            return render_template('home.html', result=out, image=inputt, input=data)
        else:
            error = "File Not Found"
            return render_template('home.html', error=error)
            
@app.route('/coder', methods=['GET', 'POST'])
def main1():
    if request.method == 'GET':
        return render_template("coder.html", error="sa")
    elif request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            cmd = ['./processing.sh upload/' + file.filename]
            subprocess.call(cmd, shell=True)
            data = glob.glob("data1/eigenfaces50/*.png")
            out = compute.compute(data, ['upload/' + file.filename.split('.')[0] + '.png'], 50)
            inputt = url_for('show', filename=file.filename.split('.')[0] + '.png')
            return render_template('coder.html', result=out, image=inputt, input=data)
        else:
            error = "File Not Found"
            return render_template('coder.html', error=error)



if __name__ == '__main__':
    app.run()

