#!/usr/bin/env bash
# Sets up the creator studio on YOUR computer (Mac or Linux; on Windows use WSL).
# Needs: git, python3 (3.10-3.12 recommended), node 18+, ffmpeg. Safe to re-run.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
DIR="${1:-$HOME/creator-studio}"; mkdir -p "$DIR"; cd "$DIR"
for r in Vibha-Ramprakash/claude-caption-styles motion-canvas/motion-canvas ManimCommunity/manim \
  Comfy-Org/ComfyUI Wan-Video/Wan2.1 Tencent-Hunyuan/HunyuanVideo Lightricks/LTX-Video \
  facebookresearch/sam2 PeterL1n/RobustVideoMatting danielgatis/rembg xinntao/Real-ESRGAN \
  hzwer/Practical-RIFE WyattBlue/auto-editor m-bain/whisperX harry0703/MoneyPrinterTurbo; do
  n="${r#*/}"; [ -d "$n" ] || git clone --depth 1 "https://github.com/$r" "$n"
done
# Light tools that work on any laptop (no GPU needed)
python3 -m venv .venv && . .venv/bin/activate
pip install -U pip auto-editor "rembg[cpu,cli]" whisperx google-api-python-client google-auth-oauthlib
# Claude Code skills
mkdir -p ~/.claude/skills
[ -d ~/.claude/skills/captions ] || cp -r claude-caption-styles ~/.claude/skills/captions
(cd ~/.claude/skills/captions && npm install)
[ -d ~/.claude/skills/youtube ] || cp -r "$HERE/skills/youtube" ~/.claude/skills/youtube
echo "Done. Activate tools with: source $DIR/.venv/bin/activate"
echo "GPU tools (ComfyUI, Wan2.1, HunyuanVideo, LTX-Video, SAM2, Real-ESRGAN, RIFE): follow each repo's README; they need an NVIDIA GPU (12-24 GB+) or a rented cloud GPU."
