# +1 Tank Evolution like counter

Every 30 minutes a GitHub Action asks Roblox for the game's like count and saves it in `likes.json`.
The game's lobby board (the like goal) reads that file, because a Roblox server can't call roblox.com itself.

It uses no tokens, no secrets and no Gist. The workflow commits `likes.json` into this repo with GitHub's built-in permission.

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
