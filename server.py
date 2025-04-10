from flask import render_template, Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', path=request.path)


@app.route('/advices')
def advices():
    return render_template('advices.html', path=request.path)


@app.route('/wardrobe')
def wardrobe():
    return render_template('wardrobe.html', path=request.path)


@app.route('/look')
def look():
    return render_template('look.html', path=request.path)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
