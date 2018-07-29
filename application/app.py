from flask import Flask, render_template, request
from selector import selector

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
        market = request.form['market']
        print (risk)
        selection = selector(risk)
        return render_template('results.html', portfolio_name=portfolio_name, risk = risk, market=market, selection=selection)
    except KeyError:
        print("Page has failed - please go back")

if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug=True)
