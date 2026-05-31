from flask import Flask, render_template, request
from collections import Counter, defaultdict
import re
import os

app = Flask(__name__)


DEFAULT_DATA = """
🔆3439260期 4+1+4=9 小单
🔆3439261期 0+6+6=12 小双
🔆3439262期 1+3+9=13 小单
🔆3439263期 7+9+4=20 大双
🔆3439264期 5+6+5=16 大双
🔆3439265期 4+9+4=17 大单
🔆3439266期 1+5+2=8 小双
🔆3439267期 1+2+7=10 小双
🔆3439268期 6+7+5=18 大双
🔆3439269期 7+1+9=17 大单
🔆3439270期 0+8+9=17 大单
🔆3439271期 0+5+8=13 小单
🔆3439272期 5+9+3=17 大单
🔆3439273期 5+8+1=14 大双
🔆3439274期 5+7+6=18 大双
🔆3439275期 4+9+4=17 大单
🔆3439276期 3+1+8=12 小双
🔆3439277期 6+7+3=16 大双
🔆3439278期 1+0+9=10 小双
🔆3439279期 1+3+2=6 小双
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
