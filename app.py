"""Web application for XFormTest

http://xform-test.pma2020.org
"""
import platform
import os
import flask
from flask import Flask, render_template, request
# noinspection PyProtectedMember
from static_methods import _run_background_process
from werkzeug.utils import secure_filename

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

is_windows = platform.system() == 'Windows'
path_char = '\\' if is_windows else '/'


@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET':
        return render_template('index.html')
    else:
        try:
            file = request.files['xform-file']
            filename = secure_filename(file.filename)
            upload_folder = basedir + path_char + 'temp_uploads'
            file_path = os.path.join(upload_folder, filename)

            if os.path.exists(file_path):
                os.remove(file_path)

            try:
                file.save(file_path)
            except FileNotFoundError:
                os.mkdir(upload_folder)
                file.save(file_path)

            options_list = request.form.getlist('options[]')
            options = " ".join(options_list)

            command = "python -m qtools2.convert "+options+" "+file_path
            stdout, stderr = _run_background_process(command)
            return render_template('index.html', stderr=stderr, stdout=stdout)

        except Exception as err:
            msg = 'An unexpected error occurred:\n\n' + str(err)
            return render_template('index.html', stderr=msg)


if __name__ == '__main__':
    app.run(debug=True)
