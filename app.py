from flask import Flask, render_template, request
from helpers.parseURL import parseURL

app = Flask(__name__)

@app.route("/") 
def home(): 
    return render_template("home.html")

@app.route("/download", methods=['GET', 'POST']) 
def download():
    url = request.form['url']
    data = parseURL(url)
    return render_template("download_page.html", data=data) 

if __name__ == "__main__": 
    app.run(debug=False) 
