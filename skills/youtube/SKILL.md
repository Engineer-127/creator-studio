---
name: youtube
description: "Manage the user's own YouTube channel for free through the official YouTube Data API: upload or schedule videos and Shorts, update titles/descriptions/tags, see channel and per-video stats, read unanswered comments and reply. Trigger on /youtube, 'upload to youtube', 'schedule my short', 'how are my videos doing', 'reply to youtube comments'."
---

# /youtube: free YouTube channel manager

Uses `scripts/yt.py` (official Google API, free daily quota of 10,000 units: an upload costs ~1,600, so about 6 uploads/day; reading stats and comments is cheap).

## One-time setup (walk the user through it)
1. Go to console.cloud.google.com → create a project → "APIs & Services" → enable **YouTube Data API v3**.
2. "OAuth consent screen" → External → add the user's own Google account as a **test user**.
3. "Credentials" → Create credentials → **OAuth client ID** → type **Desktop app** → download the JSON.
4. Save it as `~/.config/yt-skill/client_secret.json`.
5. Run `python3 scripts/yt.py auth` once; a browser opens to approve. The token is saved to `~/.config/yt-skill/token.json`. Never print or share either file.

Install deps if missing: `pip install google-api-python-client google-auth-oauthlib`

## Commands
| Command | What it does |
|---|---|
| `yt.py channel` | Subscribers, total views, video count |
| `yt.py videos [--n 20]` | Recent uploads with views, likes, comments |
| `yt.py upload FILE --title T [--desc D] [--tags a,b] [--privacy private\|unlisted\|public] [--at 2026-11-20T18:30:00+05:30] [--thumb img.jpg]` | Upload. `--at` schedules it (video stays private until then). Vertical ≤3 min = Short; add `#Shorts` to the title or description |
| `yt.py update VIDEO_ID [--title] [--desc] [--tags]` | Edit metadata |
| `yt.py comments [--n 30] [--unanswered]` | Latest comments on the channel |
| `yt.py reply COMMENT_ID "text"` | Reply to a comment |

## Rules
- **Always show the user the exact title, description, tags, privacy and time, and get a yes before `upload`, `update` or `reply`.** These are public actions.
- Default privacy is `private` unless the user says otherwise.
- Write replies in the creator's voice, short and human. Never mass-reply with the same text (YouTube treats it as spam).
- For titles: lead with the hook, under ~60 characters, no clickbait that the video doesn't deliver.
