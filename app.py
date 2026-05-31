from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <body style="
        background:#0d1117;
        color:white;
        font-family:Arial;
        text-align:center;
        padding-top:100px;
    ">
        <h1>⚡ Prediction Web</h1>
        <h2>Connected Successfully</h2>
        <p>Dark Premium Version Loading...</p>
    </body>
    """


if __name__ == "__main__":
    app.run()
