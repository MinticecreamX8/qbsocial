import requests

KEY_FILE = "key.txt"


def load_key():
    try:
        with open(KEY_FILE, "r") as f:
            return f.read().strip()
    except:
        return None


def search_twitter(topic):
    token = load_key()

    if not token:
        return ["No API key found in key.txt. go to https://developer.x.com, sign in and get an API key. then, type it in the 'key' tab in the top corner, next to 'feed'."]

    url = "https://api.twitter.com/2/tweets/search/recent"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "query": topic,
        "max_results": 10,
        "tweet.fields": "text"
    }

    try:
        r = requests.get(url, headers=headers, params=params)

        if r.status_code != 200:
            return [f"API error {r.status_code}: {r.text}"]

        data = r.json()
        tweets = data.get("data", [])

        return [t["text"] for t in tweets] if tweets else ["No results found"]

    except Exception as e:
        return [f"Request failed: {e}"]