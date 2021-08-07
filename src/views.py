#!/usr/bin/python3
# coding=utf-8
# Authors: Isidora Jeknic, Iuliia Zaitova, Kirstin Kolmorgen, Sharmila Upadhyaya
# Emails:  {shup00001}@stud.uni-saarland.de, {s8iuzait}@stud.uni-saarland.de,
# {s8kikolm}@stud.uni-saarland.de,  {shup00001}@stud.uni-saarland.de
# Organization: Universität des Saarlandes
# Copyright 2020 Sharmila Upadhyaya
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This is the main flask app
"""

import os
from shutil import copy
import urllib.request
import sys

from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import main
from flask import Markup
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
from flask import Flask

UPLOAD_FOLDER = 'src/static/'
tmp_fol = "src/tmp/"
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#temporary folder to hold images being uploaded created if not.
try:
    os.mkdir(tmp_fol)
except:
    filelist = [ f for f in os.listdir(tmp_fol) ]
    for f in filelist:
        os.remove(os.path.join(tmp_fol, f))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def result_parsing(result):
    """
    function to take the result and clear the html tags from joke
    Params:
    result (dict) : caption, question and joke for an image.
    Returns:
    list: list of joke
    """
    result_final = []
    result["jokes"] = {i: [each.lower().replace("because"," ") if ii!= 0 else each for ii, each in enumerate(joke)] for i, joke in result["jokes"].items()}
    result_final.append(Markup("<b>Joke:</b> " + "? Because ".join(list(result["jokes"].values())[0][:2])))
    return result_final 

@app.route('/')
def upload_form():
    return render_template('upload_image.html')

@app.route('/', methods=['POST'])
def upload_image():
    
    #check if file is uploaded
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    #check if file name exists
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    #check if file is image
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Image successfully uploaded and displayed below')
        copy(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(tmp_fol, filename))
        # send file path to the main pipeline
        result = main.main(tmp_fol)
        result = result_parsing(result)
        os.remove(os.path.join(tmp_fol, filename))
        return render_template('upload_image.html', filename=filename, captions=result)

    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=filename), code=301)

if __name__ == "__main__":
    app.run()
