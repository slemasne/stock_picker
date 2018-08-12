from flask import Flask, render_template, request
from selector import stockStats, loadData, columns, url

app = Flask(__name__)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/results', methods=["POST"])
def results():
    try:
        request.method == "POST"
        risk = request.form['risk']
        sector = request.form['sector']
        result_count = request.form.get("number")
        print(request.form)

        ticker_list = loadData(url).random_symbols(sector, int(result_count))

        df_stats = stockStats(ticker_list, columns).stock_stats()


        return render_template('results.html', risk = risk, sector=sector, table = df_stats.to_html(classes="table-striped"))
    except KeyError:
        print("Page has failed - please go back")

if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug=True)