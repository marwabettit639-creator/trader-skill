"""
Trading 212 read-only connection.
GET requests only. No order placement or account modifications.
"""

import os
import json
import base64
import urllib.request


class Trading212ReadOnly:

    def __init__(self):
        self.api_key = os.environ["T212_API_KEY"]
        self.api_secret = os.environ["T212_API_SECRET"]

        environment = os.getenv("T212_ENV", "demo").lower()

        if environment == "live":
            self.base_url = "https://live.trading212.com/api/v0"
        else:
            self.base_url = "https://demo.trading212.com/api/v0"

        credentials = f"{self.api_key}:{self.api_secret}"
        encoded = base64.b64encode(
            credentials.encode()
        ).decode()

        self.headers = {
            "Authorization": f"Basic {encoded}",
            "Accept": "application/json"
        }

    def _get(self, endpoint):
        request = urllib.request.Request(
            self.base_url + endpoint,
            headers=self.headers,
            method="GET"
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode())

    def account_summary(self):
        return self._get("/equity/account/summary")

    def positions(self):
        return self._get("/equity/positions")

    def open_orders(self):
        return self._get("/equity/orders")


if __name__ == "__main__":
    print("Trading 212 read-only module created.")