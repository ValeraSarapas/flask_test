from flask import Flask,request,jsonify,abort, redirect, url_for,render_template,send_file
import joblib
import numpy as np

app = Flask(__name__)

knn= joblib.load('knn.pkl')

@app.route("/")
def hello():
 #   print('1+2')
    return "<h1>Hello My very best Friend!!!!</h1>"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

def mean (numbers):
    return float(sum(numbers))/max(len(numbers),1)

@app.route('/awg/<nums>')
def show_awg(nums):
    nums = nums.split(',')
    mean_nums = mean([float(num) for num in nums])
    print(mean_nums)
    # show the user profile for that user
    return 'Awg %s' % mean_nums

@app.route('/iris/<params>')
def iris(params):
    nums = params.split(',')
    params = [float(num) for num in nums]
     
    predict = knn.predict(np.array(params).reshape(1,-1))
    return 'Predict %s' % predict

@app.route('/show_iris/')
def show_iris():
    return '<img src="/static/setosa.jpg" alt="setosa">'

@app.route('/iris_post_test/', methods=['POST'])
def iris_post_test():
    print("-------------------------")
    print("Method:",request.method)
    print("Header:",request.headers)
    print("Mimetype:",request.mimetype)
    print("Data:",request.data)

    content = request.get_json()
    print("Content: ",content) # Do your processing
    return jsonify(content)

@app.route('/badrequest400')
def bad_request():
    return abort(400)

@app.route('/iris_post/', methods=['POST'])
def iris_post():
    print("-------------------------")
 
    try:
        content = request.get_json()
        print("Content: ",content)
        params = content['flower'].split(',')
        params = [float(num) for num in params]
        
        predict = knn.predict(np.array(params).reshape(1,-1))
        predict= {'class':str(predict[0])}
    except:
        return redirect(url_for('bad_request'))
    return jsonify(predict)
    
from flask_wtf import FlaskForm
from wtforms import StringField,FileField
from wtforms.validators import DataRequired

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField()

from werkzeug.utils import secure_filename
import os
import pandas as pd 

@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        print("___________________________")
        #print(form.name.data)

        f = form.file.data
        #filename = secure_filename(f.filename)
        filename = form.name.data+'.csv'
#        print("File name:",filename)
#        print("File:",f)
#        print("form name:",form.file.data)

     #   f.save(os.path.join(
     #       filename
     #   ))
        df = pd.read_csv(f,header = None, error_bad_lines=False)
        print(df.head())

        predict = knn.predict(df)

        print(predict)

        result = pd.DataFrame(predict)
        result.to_csv(filename,index=False)

        return send_file(filename,
                     mimetype='text/csv',
                     attachment_filename=filename,
                     as_attachment=True)

#    return render_template('submit.html', form=form)
#        return('file uploded',str(form.name.data))
    return render_template('submit.html', form=form)

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
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
            filename = secure_filename(file.filename+'uploaded')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return ('file uploaded')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''