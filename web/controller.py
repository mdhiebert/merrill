import flask

app = flask(__name__)

@app.route("/")
def index():
    return 'Index Page'