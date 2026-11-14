# Creator Studio

My setup for making Reels/Shorts with Claude and open-source video tools, and managing Instagram + YouTube for free.

- **[PLAYBOOK.md](PLAYBOOK.md)**: what each tool does, the production pipeline, account skills, growth routine
- **[setup-my-computer.sh](setup-my-computer.sh)**: downloads the 15 tool repos (listed in `repos.txt`), installs the CPU tools and the Claude skills
- **[skills/youtube](skills/youtube)**: `/youtube` Claude skill (upload/schedule, stats, comment replies) using the free YouTube Data API

## Quick start
```bash
git clone https://github.com/Engineer-127/creator-studio ~/creator-studio
cd ~/creator-studio && ./setup-my-computer.sh ~/creator-studio
```
Then restart Claude Code and try `/captions` and `/youtube`.
