import csv
import os
from flask import Flask, redirect, render_template, request, url_for, send_from_directory
from io import StringIO
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:\Final Project\output'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.run(debug=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/",methods=["GET", "POST"])
def home():
     if request.method == "GET":
         return render_template("final.html")
     # Get file to be uploaded
     f = request.files['file'] 
     # if valid 
     if f and allowed_file(f.filename):
          filename = secure_filename(f.filename)
          
          # get file names to split csv into good and bad data
          bad_filename = f'{filename.split(".")[0]}_bad.csv'
          good_filename = f'{filename.split(".")[0]}_good.csv'
          
          # make sure data is of string type
          data = StringIO(f.read().decode('utf-8-sig')) 
          
          # get info to dictionary 
          rows = csv.DictReader(data)
          
          # Get keys of dictionary
          keys = rows.fieldnames
          
          # Open two files to write good and bad data
          with open(os.path.join('output', good_filename), 'w', newline='') as g, open(os.path.join('output', bad_filename), 'w', newline='') as b :
               
               # get writer and writer header row for good
               g_writer = csv.DictWriter(g, keys)
               g_writer.writeheader()
               
               # get writer and writer header row for bad
               b_writer = csv.DictWriter(b, keys)
               b_writer.writeheader()
               
               # if the start time zeros bad data write to file
               for row in rows:
                    if row["START TIME"] == "0:00:00":
                         b_writer.writerow(row)
                    # else it's good data write to file     
                    else:
                         g_writer.writerow(row)
                        
          # auto download good file
          return redirect(url_for('download_file', name=good_filename)) 

def new_func(f):
    return StringIO(f.read().decode('utf-8-sig'))    

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)





