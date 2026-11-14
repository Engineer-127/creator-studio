#!/usr/bin/env bash
# Sets up the creator studio on YOUR computer (Mac or Linux; on Windows use WSL).
# Needs: git, Python 3.12 (Mac: brew install python@3.12), node 18+, ffmpeg. Safe to re-run.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
DIR="${1:-$HOME/creator-studio}"; mkdir -p "$DIR"; cd "$DIR"
for r in Vibha-Ramprakash/claude-caption-styles motion-canvas/motion-canvas ManimCommunity/manim \
  Comfy-Org/ComfyUI Wan-Video/Wan2.1 Tencent-Hunyuan/HunyuanVideo Lightricks/LTX-Video \
  facebookresearch/sam2 PeterL1n/RobustVideoMatting danielgatis/rembg xinntao/Real-ESRGAN \
  hzwer/Practical-RIFE WyattBlue/auto-editor m-bain/whisperX harry0703/MoneyPrinterTurbo; do
  n="${r#*/}"; [ -d "$n" ] || git clone --depth 1 "https://github.com/$r" "$n"
done
# Light tools that work on any laptop (no GPU needed).
# AI tools (whisperx, rembg...) don't support the newest Python yet, so use 3.12/3.11/3.10.
PY=""
for v in 3.12 3.11 3.10; do command -v "python$v" >/dev/null && { PY="python$v"; break; }; done
if [ -z "$PY" ]; then
  echo "Python 3.12 not found. Install it first:  brew install python@3.12   (then re-run this script)"; exit 1
fi
# Rebuild .venv if an earlier run made it with a different Python
if [ -x .venv/bin/python ] && [ "$(.venv/bin/python -c 'import sys;print(f"{sys.version_info[0]}.{sys.version_info[1]}")')" != "${PY#python}" ]; then
  rm -rf .venv
fi
[ -d .venv ] || "$PY" -m venv .venv
. .venv/bin/activate
pip install -U pip
FAILED=""
for pkg in auto-editor "rembg[cpu,cli]" whisperx google-api-python-client google-auth-oauthlib; do
  echo "== installing $pkg"; pip install -U "$pkg" || FAILED="$FAILED $pkg"
done
# Claude Code skills
mkdir -p ~/.claude/skills
[ -d ~/.claude/skills/captions ] || cp -r claude-caption-styles ~/.claude/skills/captions
(cd ~/.claude/skills/captions && npm install)
[ -d ~/.claude/skills/youtube ] || cp -r "$HERE/skills/youtube" ~/.claude/skills/youtube
[ -n "$FAILED" ] && echo "WARNING: these did not install:$FAILED (everything else is fine)"
echo "Done. Activate tools with: source $DIR/.venv/bin/activate"
echo "GPU tools (ComfyUI, Wan2.1, HunyuanVideo, LTX-Video, SAM2, Real-ESRGAN, RIFE): follow each repo's README; they need an NVIDIA GPU (12-24 GB+) or a rented cloud GPU."
