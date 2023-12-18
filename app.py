import csv
from io import StringIO
from flask import Flask, flash, redirect, render_template, request, session
from fileinput import filename 

app = Flask(__name__)


@app.route("/",methods=["GET", "POST"])
def home():
    if request.method == "GET":
         return render_template("final.html")
    f = request.files['file'] 
    data = StringIO(f.read().decode('utf-8'))  
    list1 = []
    name = csv.DictReader(data)
    for row in name:
         list1.append(row)
    return render_template("success.html", name=list1)
