from flask import Flask, render_template, request, make_response
from selector import stockSelector, loadData, url
from datetime import  datetime

app = Flask(__name__)


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/table')
def table():
    sector = request.cookies.get('sector')

    print ("This is the cookie: " + sector)

    data_df = loadData(sector, url).stock_stats_for_webpage()
    return render_template('table.html', table = data_df.to_html(classes="table-striped"))

@app.route('/results', methods=["POST"])
def results():
    try:
        request.method == "POST"

        risk = request.form['risk']
        sector = request.form['sector']
        strategy = request.form['strategy']
        result_count = request.form.get("number")

        data_df = stockSelector(int(risk), sector, strategy, int(result_count))
        html_risk = (lambda x: "Low" if int(x) == 0 else "Medium" if int(x) == 1 else "High" if int(x) == 2 else "Very High")

        df_value =  list(data_df.values.tolist())

        print (data_df.columns)
        print (df_value)

        time = datetime.now().strftime('%I:%M%p on %b-%d')

        response = make_response(render_template('results.html', risk = html_risk(risk), sector=sector, strategy = strategy, table = data_df.to_html(classes="table-striped"), time = time, df_value=df_value))
        response.set_cookie('sector', sector)

        return response

    except:

        return render_template('error.html')

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'key'
    app.run()
    app.run(debug=True)
