from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def home():
    return f'Site  Construction'



if __name__ == '__main__':
   app.run(debug=True)