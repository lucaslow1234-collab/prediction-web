from flask import Flask, render_template
from collections import Counter, defaultdict
import re
import os

app = Flask(__name__)

raw_data = """
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

history = re.findall(r'[大小单双]{2}', raw_data)

CATS = ["小单", "大单", "小双", "大双"]


def trend_model(history):
    score = Counter()
    recent = history[-8:]

    for i, cat in enumerate(reversed(recent)):
        score[cat] += (8 - i)

    return score


def transition_model(history):
    score = Counter()
    latest = history[-1]

    transitions = defaultdict(Counter)

    for i in range(len(history)-1):
        transitions[
            history[i]
        ][
            history[i+1]
        ] += 1

    for nxt, cnt in transitions[
        latest
    ].items():

        score[nxt] += cnt * 3

    return score


def anti_streak_model(history):
    score = Counter()
    latest = history[-1]

    streak = 1

    for i in range(len(history)-2, -1, -1):
        if history[i] == latest:
            streak += 1
        else:
            break

    if streak >= 2:
        score[latest] -= streak * 10

    return score


def split_model(history):
    score = Counter()
    recent = history[-10:]

    big = sum("大" in x for x in recent)
    even = sum("双" in x for x in recent)

    size_pref = "小" if big >= 7 else "大"
    parity_pref = "单" if even >= 7 else "双"

    score[size_pref + parity_pref] += 10

    return score


def predict(history, weights):

    total = Counter()

    models = {
        "trend": trend_model(history),
        "transition": transition_model(history),
        "split": split_model(history),
        "streak": anti_streak_model(history)
    }

    for name, weight in weights.items():
        for k, v in models[name].items():
            total[k] += v * weight

    ranked = sorted(
        total.items(),
        key=lambda x: x[1],
        reverse=True
    )

    confidence = max(
        0,
        round(
            ranked[0][1] - ranked[2][1],
            2
        )
    )

    return ranked, confidence


def evaluate(weights):

    wins = 0
    total = 0
    history_log = []

    for i in range(10, len(history)):

        ranked, conf = predict(
            history[:i],
            weights
        )

        if conf < 3:
            continue

        picks = [
            ranked[0][0],
            ranked[1][0]
        ]

        actual = history[i]

        win = actual in picks

        history_log.append({
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

    return {
        "rate": round(rate, 2),
        "wins": wins,
        "total": total,
        "log": history_log
    }


CONFIGS = [
    {
        "trend": 1,
        "transition": 2,
        "split": 4,
        "streak": 2
    },
    {
        "trend": 2,
        "transition": 4,
        "split": 5,
        "streak": 3
    },
    {
        "trend": 3,
        "transition": 2,
        "split": 3,
        "streak": 4
    }
]

results = []

for cfg in CONFIGS:
    r = evaluate(cfg)
    r["weights"] = cfg
    results.append(r)

best = sorted(
    results,
    key=lambda x: x["rate"],
    reverse=True
)[0]


@app.route("/")
def home():

    ranked, conf = predict(
        history,
        best["weights"]
    )

    prediction = {
        "round": "NEXT",
        "main": ranked[0][0],
        "second": ranked[1][0],
        "defense": ranked[2][0],
        "kill": ranked[-1][0],
        "confidence": conf,
        "accuracy": f'{best["rate"]}%'
    }

    return render_template(
        "index.html",
        data=prediction,
        logs=best["log"][-8:]
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
