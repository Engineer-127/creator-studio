#!/usr/bin/env python3
"""Free YouTube channel manager (official YouTube Data API v3). See SKILL.md for setup."""
import argparse, os, sys
from pathlib import Path

CFG = Path(os.environ.get("YT_SKILL_DIR", Path.home() / ".config" / "yt-skill"))
SECRET, TOKEN = CFG / "client_secret.json", CFG / "token.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl", "https://www.googleapis.com/auth/youtube.upload"]

def service():
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        sys.exit("Missing packages: pip install google-api-python-client google-auth-oauthlib")
    creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES) if TOKEN.exists() else None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not SECRET.exists():
                sys.exit(f"Put your OAuth Desktop client JSON at {SECRET} (see SKILL.md).")
            creds = InstalledAppFlow.from_client_secrets_file(str(SECRET), SCOPES).run_local_server(port=0)
        CFG.mkdir(parents=True, exist_ok=True)
        TOKEN.write_text(creds.to_json()); os.chmod(TOKEN, 0o600)
    return build("youtube", "v3", credentials=creds)

def my_channel(yt):
    return yt.channels().list(part="snippet,statistics,contentDetails", mine=True).execute()["items"][0]

def cmd_channel(yt, a):
    c = my_channel(yt); s = c["statistics"]
    print(f'{c["snippet"]["title"]}  ({c["id"]})')
    print(f'subscribers {s.get("subscriberCount","hidden")} | views {s["viewCount"]} | videos {s["videoCount"]}')

def cmd_videos(yt, a):
    up = my_channel(yt)["contentDetails"]["relatedPlaylists"]["uploads"]
    items = yt.playlistItems().list(part="contentDetails", playlistId=up, maxResults=min(a.n, 50)).execute()["items"]
    ids = [i["contentDetails"]["videoId"] for i in items]
    if not ids: return print("No videos yet.")
    for v in yt.videos().list(part="snippet,statistics,status", id=",".join(ids)).execute()["items"]:
        s = v["statistics"]
        print(f'{v["id"]}  {v["snippet"]["publishedAt"][:10]}  {v["status"]["privacyStatus"]:8}  '
              f'views {s.get("viewCount",0):>7}  likes {s.get("likeCount",0):>5}  comments {s.get("commentCount",0):>4}  {v["snippet"]["title"]}')

def cmd_upload(yt, a):
    from googleapiclient.http import MediaFileUpload
    status = {"privacyStatus": "private" if a.at else a.privacy, "selfDeclaredMadeForKids": False}
    if a.at: status["publishAt"] = a.at
    body = {"snippet": {"title": a.title, "description": a.desc or "", "tags": [t.strip() for t in (a.tags or "").split(",") if t.strip()], "categoryId": a.category}, "status": status}
    req = yt.videos().insert(part="snippet,status", body=body, media_body=MediaFileUpload(a.file, chunksize=8 << 20, resumable=True))
    resp = None
    while resp is None:
        st, resp = req.next_chunk()
        if st: print(f"uploading {int(st.progress()*100)}%", flush=True)
    vid = resp["id"]; print(f"Uploaded: https://youtu.be/{vid}" + (f" (scheduled {a.at})" if a.at else ""))
    if a.thumb:
        yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(a.thumb)).execute(); print("Thumbnail set.")

def cmd_update(yt, a):
    v = yt.videos().list(part="snippet", id=a.video_id).execute()["items"][0]; sn = v["snippet"]
    if a.title: sn["title"] = a.title
    if a.desc is not None: sn["description"] = a.desc
    if a.tags is not None: sn["tags"] = [t.strip() for t in a.tags.split(",") if t.strip()]
    yt.videos().update(part="snippet", body={"id": a.video_id, "snippet": sn}).execute(); print("Updated.")

def cmd_comments(yt, a):
    cid = my_channel(yt)["id"]
    r = yt.commentThreads().list(part="snippet,replies", allThreadsRelatedToChannelId=cid, maxResults=min(a.n, 100), order="time", textFormat="plainText").execute()
    for t in r.get("items", []):
        top = t["snippet"]["topLevelComment"]; s = top["snippet"]
        answered = any(x["snippet"].get("authorChannelId", {}).get("value") == cid for x in t.get("replies", {}).get("comments", []))
        if a.unanswered and (answered or s.get("authorChannelId", {}).get("value") == cid): continue
        print(f'[{top["id"]}] video {s["videoId"]} | {s["authorDisplayName"]}: {s["textDisplay"][:300]}' + ("  (replied)" if answered else ""))

def cmd_reply(yt, a):
    yt.comments().insert(part="snippet", body={"snippet": {"parentId": a.comment_id, "textOriginal": a.text}}).execute(); print("Replied.")

p = argparse.ArgumentParser(); sp = p.add_subparsers(dest="cmd", required=True)
sp.add_parser("auth"); sp.add_parser("channel")
x = sp.add_parser("videos"); x.add_argument("--n", type=int, default=20)
x = sp.add_parser("upload"); x.add_argument("file"); x.add_argument("--title", required=True); x.add_argument("--desc"); x.add_argument("--tags")
x.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"]); x.add_argument("--at", help="RFC3339 publish time"); x.add_argument("--thumb"); x.add_argument("--category", default="22")
x = sp.add_parser("update"); x.add_argument("video_id"); x.add_argument("--title"); x.add_argument("--desc"); x.add_argument("--tags")
x = sp.add_parser("comments"); x.add_argument("--n", type=int, default=30); x.add_argument("--unanswered", action="store_true")
x = sp.add_parser("reply"); x.add_argument("comment_id"); x.add_argument("text")
a = p.parse_args(); yt = service()
if a.cmd == "auth": print("Authorized."); cmd_channel(yt, a)
else: globals()["cmd_" + a.cmd](yt, a)
