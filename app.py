from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route("/")
def home():

    fake_prediction = {
        "round": "3439299",
        "main": "大双",
        "second": "小单",
        "defense": "小双",
        "kill": "大单",
        "confidence": random.randint(65, 90),
        "accuracy": "63.4%"
    }

    return render_template(
        "index.html",
        data=fake_prediction
    )


if __name__ == "__main__":
    import os

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
