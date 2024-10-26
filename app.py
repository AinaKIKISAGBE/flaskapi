
from flask import Flask
app = Flask(__name__)

@app.route('/')
def welcome():
    return "Hello, I'm Aina KIKI-SAGBE you teacher, this your first test flask"


if __name__=='__main__':
    app.run(host='0.0.0.0', 
#            port=5000, 
#            debug=True
            )


