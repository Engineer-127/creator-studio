# Creator Studio Playbook

How to use the 15 repos + Claude skills to make high-retention Reels/Shorts, and run your Instagram + YouTube for free.

> Honest note: no tool guarantees millions of followers. The algorithm rewards **watch time, rewatches, shares and saves**. These tools make videos faster and better looking. The idea, the hook and posting consistently are what make them grow.

---

## 1. What each repo is for

| Repo | Job in your workflow | Needs GPU? |
|---|---|---|
| **auto-editor** | Removes silences/pauses → fast jump-cut pacing | No |
| **whisperX** | Accurate transcripts + word timings (captions, YouTube subtitles, repurposing) | No (faster with GPU) |
| **claude-caption-styles** | `/captions pop-sticker` → animated captions on your video | No |
| **rembg** | Cut you out of a photo for thumbnails / cover images | No |
| **manim** | Math/science/tech explainer animations | No |
| **motion-canvas** | Animated text, diagrams, infographics, intros (code → video) | No |
| **RobustVideoMatting** | Remove video background (green-screen without a green screen) | Better with GPU |
| **sam2** | Track/cut out any object in video (text-behind-you effect, object VFX) | Yes |
| **Real-ESRGAN** | Upscale/sharpen low-res clips and thumbnails | Better with GPU |
| **Practical-RIFE** | Smooth slow-motion / 60fps from 30fps | Better with GPU |
| **ComfyUI** | Visual node app to run all the AI image/video models below | Yes |
| **Wan2.1 / HunyuanVideo / LTX-Video** | AI-generated B-roll, transitions, cinematic shots from text or an image | Yes (LTX-Video is the lightest) |
| **MoneyPrinterTurbo** | Topic → full faceless short (script, stock footage, voice, subs). Use for drafts/ideas, not mass-posting | No |

**No NVIDIA GPU?** Rent one only when needed (RunPod, Vast.ai, Google Colab), roughly $0.3–1/hour. Do the CPU steps on your laptop.

---

## 2. The production pipeline (one Reel/Short, ~30–60 min)

```
Idea + hook → Shoot → auto-editor → (VFX) → captions → motion graphics → export → post
```

**Step 1. Hook first.** Write the first line before anything else. It must create curiosity or promise a payoff in under 2 seconds.
Ask Claude: *"Give me 10 hooks for a reel about <topic>, under 10 words each."*

**Step 2. Shoot.** 9:16 vertical, 1080×1920, face lit from a window, phone mic close or a cheap lav. iPhone: Settings → Camera → Formats → Most Compatible (avoids washed-out HDR).

**Step 3. Cut the dead air.**
```bash
auto-editor raw.mp4 --margin 0.15sec -o cut.mp4
```

**Step 4. Optional VFX.**
- Background swap: RobustVideoMatting → put yourself on any scene.
- Text behind you: sam2 mask of yourself → place text between background and you.
- AI B-roll: in ComfyUI load an LTX-Video or Wan2.1 workflow, prompt e.g. *"cinematic drone shot over neon city at night, 9:16"*, generate 3–5 sec clips.
- Slow-mo: Practical-RIFE on action clips. Upscale old/low-res footage with Real-ESRGAN.

**Step 5. Captions (in Claude Code).** Drag `cut.mp4` in and type:
```
/captions pop-sticker with coral highlights
```
Pick one style per series so your videos are recognisable.

**Step 6. Motion graphics.** Ask Claude to write a motion-canvas (or manim) scene: *"animated stat counter from 0 to 1M with a pop at the end, 1080x1920, 3 seconds"*. Use for intros, numbers, lists, diagrams.

**Step 7. Thumbnail / cover.** rembg to cut yourself out → big 3–4 word text → bright background.
```bash
rembg i me.jpg me_cutout.png
```

**Step 8. Post** with the skills in section 3.

---

## 3. Running your accounts for free (Claude skills)

| Skill | What it does | Cost | Setup |
|---|---|---|---|
| **/youtube** (built for you, in `skills/youtube`) | Upload/schedule Shorts & videos, edit titles, stats, read + reply to comments | Free (YouTube Data API: 10,000 units/day ≈ 6 uploads/day) | Google Cloud project → enable YouTube Data API v3 → OAuth Desktop client → save JSON to `~/.config/yt-skill/client_secret.json` → `python3 scripts/yt.py auth` |
| **Instagram plugin** (already on your account) | Read + reply to comments and DMs, comment-to-DM automation | Free (official Instagram Graph API) | Instagram **Creator or Business** account linked to a Facebook Page → Meta developer app → access token → run `/instagram:configure` |
| **Buzzfy plugin** (already on your account) | Instagram audit, reel checkup, publish/schedule posts & carousels, answer comments | Check buzzfy.co for its free tier | `/buzzfy:get-started` (couldn't connect in this cloud session because the network blocks it, so run it from Claude desktop or the CLI on your computer) |

Example prompts once connected:
- *"How did my last 10 YouTube Shorts do? Which hook styles got the most views?"*
- *"Upload final.mp4 as a Short titled 'I tried X for 30 days' scheduled Friday 6:30pm IST, private until then."*
- *"Show unanswered comments on YouTube and Instagram and draft replies in my voice."*
- *"/buzzfy:reel-checkup my last reel: why did it flop?"*

Claude always shows you the post or reply and waits for your OK before publishing.

---

## 4. What actually grows an account

1. **Pick one niche + one format** and repeat it (e.g. "60-second AI tool demos", "tech explained with animations"). Same caption style, same intro, same thumbnail look.
2. **Hook in 1–2 sec, payoff by the end.** Cut every second that doesn't move the story (auto-editor helps).
3. **15–45 sec** for Reels/Shorts. Loop the ending into the start for rewatches.
4. **Post consistently**: 1 per day for 60–90 days beats 10 videos one week then nothing.
5. **Post the same video on Reels + Shorts** (remove watermarks between platforms).
6. **Reply to every comment in the first hour.** It boosts reach and builds community.
7. **Review weekly**: ask Claude to pull stats and find what your top 3 videos had in common, then make more of that.
8. **Avoid low-effort AI spam.** Instagram and YouTube limit reach of mass-produced, unoriginal AI content (and YouTube can demonetise it). Use AI for B-roll and polish, keep your face/voice/opinion in the video.
9. **Respect copyright.** Use licensed music (Instagram/YouTube audio libraries) and only footage you own or generated.

---

## 5. Weekly routine (example)

| Day | Task |
|---|---|
| Mon | Ask Claude for 7 ideas + hooks from last week's best performer. Write scripts. |
| Tue | Batch-shoot 4–7 videos. |
| Wed | auto-editor → captions → B-roll/motion graphics for all of them. |
| Thu | Schedule the week with /youtube and Buzzfy. |
| Daily | 15 min replying to comments and DMs with Claude. |
| Sun | Stats review: what worked, what to repeat. |
