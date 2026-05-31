from flask import Flask, render_template, request
from collections import Counter, defaultdict
import re
import os

app = Flask(__name__)


DEFAULT_DATA = """
开奖历史
🌑3439395期 5+5+2=12 小双
🌑3439396期 5+3+5=13 小单
🌑3439397期 3+9+7=19 大单
🌑3439398期 6+3+7=16 大双
🌑3439399期 9+5+6=20 大双
🌑3439400期 5+8+5=18 大双
🌑3439401期 2+0+5= 7 小单
🌑3439402期 4+9+7=20 大双
🌑3439403期 3+0+6= 9 小单
🌑3439404期 5+8+4=17 大单
🌑3439405期 3+0+0= 3 小单
🌑3439406期 9+1+2=12 小双
🌑3439407期 7+0+7=14 大双
🌑3439408期 5+3+0= 8 小双
🌑3439409期 1+2+4= 7 小单
🌑3439410期 9+6+4=19 大单
🌑3439411期 8+3+7=18 大双
🌑3439412期 8+0+2=10 小双
🌑3439413期 2+4+6=12 小双
🌑3439414期 1+7+0= 8 小双
"""


def parse_history(raw_data):
    return re.findall(
        r'[大小单双]{2}',
        raw_data
    )


def predict(history):

    score = Counter()

    if len(history) < 5:
        return [], 0

    latest = history[-1]

    # Trend
    recent = history[-8:]

    for i, cat in enumerate(
        reversed(recent)
    ):
        score[cat] += (
            8 - i
        )

    # Transition
    transitions = defaultdict(
        Counter
    )

    for i in range(
        len(history)-1
    ):
        transitions[
            history[i]
        ][
            history[i+1]
        ] += 1

    for nxt, cnt in transitions[
        latest
    ].items():

        score[nxt] += cnt * 3

    # Anti streak
    streak = 1

    for i in range(
        len(history)-2,
        -1,
        -1
    ):
        if history[i] == latest:
            streak += 1
        else:
            break

    if streak >= 2:
        score[latest] *= 0.4

    ranked = sorted(
        score.items(),
        key=lambda x: x[1],
        reverse=True
    )

    confidence = 0

    if len(ranked) >= 3:
        confidence = round(
            ranked[0][1]
            - ranked[2][1],
            2
        )

    return ranked, confidence


def backtest(history):

    wins = 0
    total = 0
    logs = []

    for i in range(
        10,
        len(history)
    ):

        ranked, conf = predict(
            history[:i]
        )

        if len(ranked) < 2:
            continue

        picks = [
            ranked[0][0],
            ranked[1][0]
        ]

        actual = history[i]

        win = (
            actual in picks
        )

        logs.append({
            "round": i,
            "actual": actual,
            "pick": picks,
            "win": win
        })

        total += 1

        if win:
            wins += 1

    rate = (
        wins / total * 100
    ) if total else 0

    return round(
        rate,
        2
    ), logs[-8:]


@app.route(
    "/",
    methods=["GET", "POST"]
)
def home():

    raw_data = DEFAULT_DATA

    if request.method == "POST":
        raw_data = request.form.get(
            "history",
            DEFAULT_DATA
        )

    history = parse_history(
        raw_data
    )

    ranked, conf = predict(
        history
    )

    rate, logs = backtest(
        history
    )

    prediction = {
        "main":
        ranked[0][0]
        if len(ranked) > 0
        else "-",

        "second":
        ranked[1][0]
        if len(ranked) > 1
        else "-",

        "defense":
        ranked[2][0]
        if len(ranked) > 2
        else "-",

        "kill":
        ranked[-1][0]
        if len(ranked) > 0
        else "-",

        "confidence":
        conf,

        "accuracy":
        str(rate) + "%"
    }

    return render_template(
        "index.html",
        data=prediction,
        logs=logs,
        raw_data=raw_data
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
