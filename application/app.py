from flask import Flask, render_template, request
from selector import stockSelector, columns

app = Flask(__name__)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/results', methods=["POST"])
def results():
    try:
        request.method == "POST"
        risk = request.form['risk']
        market = request.form['market']
        result_count = request.form.get("number")
        print(result_count)
        print (request.form)
        selector_results = stockSelector(int(result_count), columns).stock_stats()
        return render_template('results.html', risk = risk, market=market, table = selector_results.to_html(classes="table-striped"))
    except KeyError:
        print("Page has failed - please go back")

if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug=True)
