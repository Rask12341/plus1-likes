"""
Writes each game's like / dislike count into its own file:
    likes.json           +1 Tank Evolution      (universe 10764830764)
    sandworm_likes.json  +1 Sandworm Evolution  (universe 10774102472, added 2026-11-03)

Run in a loop by .github/workflows/update-likes.yml. Each game's server reads its own file from
raw.githubusercontent.com, because a Roblox server cannot call roblox.com itself.
One request asks for both games. A game the API leaves out keeps its old file; the others are still written.
Standard library only, so the workflow needs no pip install.
"""
import json
import urllib.request

GAMES = {  # universe id (public, not a secret) -> file
    10764830764: "likes.json",           # +1 Tank Evolution
    10774102472: "sandworm_likes.json",  # +1 Sandworm Evolution
}
URL = "https://games.roblox.com/v1/games/votes?universeIds=" + ",".join(str(u) for u in GAMES)


def write(path, likes, dislikes):
    try:
        with open(path) as f:
            old = json.load(f)
    except (OSError, ValueError):
        old = {}
    new = {"likes": likes, "dislikes": dislikes}
    if old == new:
        print(f"{path} unchanged: {likes} likes / {dislikes} dislikes")
        return
    with open(path, "w") as f:
        json.dump(new, f)
        f.write("\n")
    print(f"{path} updated: {old} -> {new}")


def main():
    with urllib.request.urlopen(URL, timeout=15) as r:
        data = json.load(r).get("data") or []
    rows = {row.get("id"): row for row in data if isinstance(row, dict)}
    missing = []
    for universe, path in GAMES.items():
        row = rows.get(universe)
        if not row or row.get("upVotes") is None:
            missing.append(universe)
            continue
        write(path, max(0, int(row["upVotes"])), max(0, int(row.get("downVotes") or 0)))
    if missing:
        raise SystemExit(f"votes API gave no count for {missing}: {data}")


if __name__ == "__main__":
    main()
