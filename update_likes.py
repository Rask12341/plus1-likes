"""
Writes likes.json with +1 Tank Evolution's like / dislike count.

Run every 30 minutes by .github/workflows/update-likes.yml. The game server reads the file from
raw.githubusercontent.com, because a Roblox server cannot call roblox.com itself.
Standard library only, so the workflow needs no pip install.
"""
import json
import urllib.request

UNIVERSE_ID = 10764830764  # +1 Tank Evolution (public, not a secret)
URL = f"https://games.roblox.com/v1/games/votes?universeIds={UNIVERSE_ID}"


def main():
    with urllib.request.urlopen(URL, timeout=15) as r:
        data = json.load(r).get("data") or []
    if not data or data[0].get("upVotes") is None:
        raise SystemExit(f"votes API gave no count: {data}")
    likes = max(0, int(data[0]["upVotes"]))
    dislikes = max(0, int(data[0].get("downVotes") or 0))
    try:
        with open("likes.json") as f:
            old = json.load(f)
    except (OSError, ValueError):
        old = {}
    new = {"likes": likes, "dislikes": dislikes}
    if old == new:
        print(f"unchanged: {likes} likes / {dislikes} dislikes")
        return
    with open("likes.json", "w") as f:
        json.dump(new, f)
        f.write("\n")
    print(f"updated: {old} -> {new}")


if __name__ == "__main__":
    main()
