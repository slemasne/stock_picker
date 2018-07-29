from flask import Flask, render_template, request
from selector import stock_beta, beta_list

app = Flask(__name__)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/results', methods=["POST", "GET"])
def results():
    try:
        request.method == "POST"
        risk = request.form['risk']
        market = request.form['market']
        print (request.form)
        beta = beta_list
        print (beta)
        return render_template('results.html', risk = risk, market=market, beta = beta)
    except KeyError:
        print("Page has failed - please go back")

if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug=True)
