import os
import subprocess
from flask import Flask, request, render_template
import compute
import glob

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template("home.html", error="sa")
    elif request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            cmd = ['./processing.sh upload/'+file.filename]
            subprocess.call(cmd, shell=True)
            data = glob.glob("data/*.png")
            out = compute.compute(data, ['upload/'+file.filename.split('.')[0]+'.png'])
            return render_template('home.html', result=out, image=file.filename.split('.')[0]+'.png', input=data)
        else:
            error = "File Not Found"
            return render_template('home.html', error=error)


if __name__ == '__main__':
    app.run()