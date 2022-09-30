
import flask, os, threading;from threading import Thread
from flask import *

os.system("clear")

app = Flask("Muzzoco! host")

@app.route("/")
def main():
    return render_template("index.html")



def ru():
    app.run(port="8080", host="0.0.0.0")
    

def keep_alive():
    Thread(target=ru).start()

