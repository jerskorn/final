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

summary_list = []
def summary(row):
     time = row["IDLE TIME (HH:MM:SS)"]
     (h, m, s) = time.split(':')
     decimal_idle = int(h) + int(m)/60 + int(s)/3600
     time = row["ENGINE ON TIME (HH:MM:SS)"]
     (h, m, s) = time.split(':')
     decimal_on = int(h) + int(m)/60 + int(s)/3600
     percentrun = decimal_idle/decimal_on * 100
     dictrow = {'VEHICLE':row["VEHICLE"],'DRIVER NAME':row["DRIVER NAME"],
                    'Sum of Idle Hours':round(decimal_idle, 2), 
                    'Sum of Run Hours':round(decimal_on, 2),
                    'Sum of Idle Percentage':round(percentrun, 2)}
     res = None
     for dictrows in summary_list:
               if dictrows["VEHICLE"] == dictrow["VEHICLE"]:
                    dictrows["Sum of Idle Hours"] = round(dictrows["Sum of Idle Hours"] + dictrow["Sum of Idle Hours"], 2)
                    dictrows["Sum of Run Hours"] = round(dictrows["Sum of Run Hours"] + dictrow["Sum of Run Hours"], 2)
                    dictrows["Sum of Idle Percentage"] = round(int(dictrows["Sum of Idle Hours"]) / int(dictrows["Sum of Run Hours"]) * 100, 2) 
                    res = 'yes'
                    break
     if res == None:
          summary_list.append(dictrow)




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
          good_summary = f'{filename.split(".")[0]}_summary.csv'
          
          # make sure data is of string type
          data = StringIO(f.read().decode('utf-8-sig')) 
          
          # get info to dictionary 
          rows = csv.DictReader(data)
          
          # Get keys of dictionary
          keys = rows.fieldnames
          
          # Open two files to write good and bad data
          
          #with open(os.path.join('output', good_filename), 'w', newline='') as g, open(os.path.join('output', bad_filename), 'w', newline='') as b :
          with open(os.path.join(app.config['UPLOAD_FOLDER'], good_filename), 'w', newline='') as g, open(os.path.join(app.config['UPLOAD_FOLDER'], bad_filename), 'w', newline='') as b :
               
               # get writer and writer header row for good
               g_writer = csv.DictWriter(g, keys)
               g_writer.writeheader()
               
               # get writer and writer header row for bad
               b_writer = csv.DictWriter(b, keys)
               b_writer.writeheader()
               
               # if the start time zeros bad data write to file
               for row in rows:
                    if row["START TIME"] == "0:00:00" or row["END TIME"] == "0:00:00":
                         b_writer.writerow(row)
                         # for fun and trying to figure out time
                         summary(row)
                    # else it's good data write to file     
                    else:
                         g_writer.writerow(row)
          
          #write the summary file
          fieldnames = ['VEHICLE', 'DRIVER NAME', 
                    'Sum of Idle Hours', 
                    'Sum of Run Hours',
                    'Sum of Idle Percentage']
          with open(os.path.join(app.config['UPLOAD_FOLDER'], good_summary), 'w', newline='') as s:
               s_writer = csv.DictWriter(s, fieldnames=fieldnames)
               s_writer.writeheader()
               s_writer.writerows(summary_list) 

          for items in summary_list:
               print(items)            
          # auto download good file
          return render_template("success.html", good_filename=good_filename, bad_filename=bad_filename, good_summary=good_summary)


    
      

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)





