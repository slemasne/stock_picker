from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/results', methods=["POST", "GET"])
def results():
    try:
        request.method == "POST"
        portfolio_name = request.form['portfolio_name']
        risk = request.form['risk']
        return render_template('results.html', portfolio_name=portfolio_name, risk = risk)
    except KeyError:
        print("Page has failed - please go back")

if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug=True)
