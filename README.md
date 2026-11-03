# +1 games like counter

A GitHub Action asks Roblox for each game's like count about once a minute and saves it in that game's file:

| Game | Universe | File |
| --- | --- | --- |
| +1 Tank Evolution | 10764830764 | `likes.json` |
| +1 Sandworm Evolution | 10774102472 | `sandworm_likes.json` (added 2026-11-03) |

Each game's lobby board (the like goal) reads its own file, because a Roblox server can't call roblox.com itself.
To add a game: put its universe id and a new file name in `GAMES` in `update_likes.py` and add the name to the
`for f in ...` line in the workflow. The next run creates the file.

It uses no tokens, no secrets and no Gist. The workflow commits the files into this repo with GitHub's built-in permission.

## Setup (one time, about 3 minutes)

1. On github.com: **New repository**. Name it (for example `plus1-likes`), set it to **Public** (the game can only read public files), and tick **Add a README**.
2. **Add file → Upload files**: drag in `update_likes.py` and `likes.json`, then **Commit**.
3. **Add file → Create new file**. For the name, type exactly `.github/workflows/update-likes.yml` (the slashes create the folders). Paste in the contents of that file from this folder, then **Commit**.
   (Finder hides the `.github` folder, which is why this step is done by hand.)
4. Go to **Settings → Actions → General → Workflow permissions**, choose **Read and write permissions**, and click **Save**.
5. Go to **Actions → Update like count → Run workflow** once. After it finishes, `likes.json` shows the real count.
6. Open `likes.json` and click **Raw**. Copy that address (it looks like `https://raw.githubusercontent.com/<you>/<repo>/main/likes.json`) and send it to Claude.
   It goes into `LikeGoal.Url` in `ReplicatedStorage/Shared/Data/LikeGoal`.

## Good to know

- GitHub sometimes starts scheduled runs a few minutes late. That's fine: goals are paid within a 30-minute window.
- GitHub pauses scheduled workflows in a repo with no activity for 60 days. Each changed like count is a commit, so this only happens if the count doesn't move for two months. If it does, GitHub emails you and one click re-enables it.
