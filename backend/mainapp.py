from flask import Flask
from flask import render_template
from flask import request

from calculation import parser

app = Flask(__name__)


def safe_get(key, data):
    if key in data.keys():
        return data[key]
    else:
        return None
    

@app.route('/', methods=['GET'])
def index():
    return render_template(
        "index.html",
        user_input=safe_get('user_input', request.args),
        answer=safe_get('answer', request.args)
    )


@app.route('/calc', methods=['POST'])
def calc():
    data = request.get_json()
    user_input = data['userInput']
    
    if user_input:
        try:
            return parser.process(user_input)
        except ValueError as e:
            return "Cannot process input! Received error: {0:s}".format(str(e))
    else:
        return "You didn't ask anything!"


if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' * 4
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)

