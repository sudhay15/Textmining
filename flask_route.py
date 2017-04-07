#code by sunil
# Flask program to create Rest service
# input - search string
# output - List of documents and corresponding rank values in JSON

from flask import render_template,Flask,request
app = Flask(__name__)
#from app import app
import latest

@app.route("/")
@app.route("/index/<search>", methods=['GET', 'POST'])
def index(search):
    #username = request.form['search']
    #print(search)
    #return search
    result =latest.main1(search)
    print result
    return result


if __name__ == '__main__':
    app.run(debug=True)

#end