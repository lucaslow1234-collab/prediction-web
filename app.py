from flask import Flask, render_template
import os
import random

app = Flask(__name__)

@app.route("/")
def home():

    prediction = {
        "round": "3439300",
        "main": random.choice(
            ["大单", "大双", "小单", "小双"]
        ),
        "second": random.choice(
            ["大单", "大双", "小单", "小双"]
        ),
        "defense": random.choice(
            ["大单", "大双", "小单", "小双"]
        ),
        "kill": random.choice(
            ["大单", "大双", "小单", "小双"]
        ),
        "confidence": random.randint(70, 95),
        "accuracy": "68.5%"
    }

    return render_template(
        "index.html",
        data=prediction
    )

if __name__ == "__main__":
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
