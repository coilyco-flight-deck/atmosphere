---
name: writing-bluesky
version: 1.3.0
description: Read, post, and interact with Bluesky (AT Protocol) via CLI. Use when user asks to check Bluesky, post to Bluesky, view their Bluesky timeline, search Bluesky, check Bluesky notifications, or export a full post archive. Supports timeline, posting, profile lookup, search, notifications, and archive export.
homepage: https://bsky.app
metadata:
  moltbot:
    emoji: "🦋"
    requires:
      bins: ["python3"]
---

# Bluesky CLI

Interact with Bluesky/AT Protocol from the command line.

## Setup

First-time setup requires an app password from Bluesky:
1. Go to bsky.app → Settings → Privacy and Security → App Passwords
2. Create a new app password
3. Run: `bsky login --handle yourhandle.bsky.social --password xxxx-xxxx-xxxx-xxxx`

**Security:** Password is NOT stored. The CLI exports a session token on login, which auto-refreshes. Your app password only exists in memory during login.

## Commands

```bash
# Authentication
bsky login --handle user.bsky.social --password xxxx-xxxx-xxxx-xxxx
bsky whoami

# Timeline
bsky timeline              # Show home feed (10 posts)
bsky timeline -n 20        # Show 20 posts
bsky tl                    # Alias

# Posting
bsky post "Hello world!"   # Create a post
bsky p "Short post"        # Alias
bsky post "Test" --dry-run # Preview without posting

# Version
bsky --version             # Show version

# Delete
bsky delete <post_id>      # Delete a post by ID or URL
bsky rm <url>              # Alias

# Profiles
bsky profile               # Your profile
bsky profile @someone.bsky.social

# Search
bsky search "query"        # Search posts
bsky search "offsec" -n 20

# Notifications
bsky notifications         # Likes, reposts, follows, mentions
bsky notif -n 30           # Alias with count

# Archive (full post history - public, no auth needed when --handle is given)
bsky archive                                   # your own history (requires login)
bsky archive --handle coilysiren.me            # anyone's history, no auth
bsky archive --handle someone.bsky.social --out posts.md
bsky archive --handle someone.bsky.social --format json
```

### Archive output

Default output path: `./bluesky-archive-<handle>-<YYYY-MM-DD>.<ext>`. Markdown emits one section per post (created-at header, URL, reply-to URI if any, embed type if any, then text, sorted oldest-first). JSON emits the raw record values plus metadata.

Use cases: dumping a year of posts into an Obsidian vault inbox for a later pass, auditing your own history, or pulling a public account's post stream for offline analysis.

## Output Format

Timeline and search results show:
```
@handle · Jan 25 14:30
  Post text (truncated to 200 chars)
  ❤️ likes  🔁 reposts  💬 replies
  🔗 https://bsky.app/profile/handle/post/id
```

## Installation

The script uses PEP-723 inline metadata, so `uv` resolves dependencies on first run with no persistent venv:

```bash
uv run {baseDir}/scripts/bsky.py [command]
```

If `uv` is unavailable, fall back to system Python:
```bash
pip install -r {baseDir}/requirements.txt
python3 {baseDir}/scripts/bsky.py [command]
```
