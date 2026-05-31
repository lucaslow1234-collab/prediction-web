from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Prediction Web</title>
    </head>
    <body style="
        background:#0d1117;
        color:white;
        text-align:center;
        font-family:Arial;
        padding-top:100px;
    ">
        <h1>⚡ Prediction Web</h1>
        <h2>Website Working ✅</h2>
        <p>Dark mode active</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
