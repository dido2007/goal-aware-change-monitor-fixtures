#!/usr/bin/env python3
"""Score simple change detectors on goal-labeled, synthetic page pairs."""
from html.parser import HTMLParser
import json
from pathlib import Path


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.price_cents = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id") == "current-price":
            self.price_cents = int(attrs["data-cents"])

    def handle_data(self, data):
        self.text.append(data)


def parse(html):
    page = Page()
    page.feed(html)
    if page.price_cents is None:
        raise ValueError("The current-price field is missing")
    return page.price_cents, " ".join(" ".join(page.text).split())


def summarize(fixtures):
    observations = []
    for item in fixtures:
        before_price, before_text = parse(item["before"])
        after_price, after_text = parse(item["after"])
        if (before_price != after_price) != item["notify"]:
            raise ValueError(f"Inconsistent oracle label: {item['name']}")
        observations.append({
            "case": item["name"], "should_notify": item["notify"],
            "raw_html_diff": item["before"] != item["after"],
            "visible_text_diff": before_text != after_text,
            "structured_price_diff": before_price != after_price,
        })
    scores = {}
    for method in ("raw_html_diff", "visible_text_diff", "structured_price_diff"):
        scores[method] = {
            "true_positive": sum(row[method] and row["should_notify"] for row in observations),
            "false_positive": sum(row[method] and not row["should_notify"] for row in observations),
            "false_negative": sum(not row[method] and row["should_notify"] for row in observations),
            "true_negative": sum(not row[method] and not row["should_notify"] for row in observations),
        }
    return {"goal": "Alert only when the current checkout price changes", "cases": observations, "scores": scores}


if __name__ == "__main__":
    fixtures = json.loads(Path(__file__).with_name("fixtures.json").read_text())
    print(json.dumps(summarize(fixtures), indent=2))
