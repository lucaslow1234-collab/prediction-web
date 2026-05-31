```python
import requests
import re
from bs4 import BeautifulSoup


URL = "https://t.me/s/pc28"


def fetch_history():

    response = requests.get(
        URL,
        timeout=15
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    text = soup.get_text(
        "\n",
        strip=True
    )

    matches = re.findall(
        r"(小单|大单|小双|大双)",
        text
    )

    matches = matches[-100:]

    with open(
        "history.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n".join(matches)
        )

    print(
        "Saved",
        len(matches),
        "rounds"
    )


fetch_history()
```
