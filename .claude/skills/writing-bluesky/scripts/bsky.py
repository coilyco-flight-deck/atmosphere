#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "atproto>=0.0.65,<0.1.0",
# ]
# ///
"""Bluesky CLI - bird-like interface for Bluesky/AT Protocol"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

VERSION = "1.3.0"

try:
    from atproto import Client, client_utils
except ImportError:
    print("Error: atproto not installed. Run via `uv run bsky.py` or `pip install atproto`.", file=sys.stderr)
    sys.exit(1)

CONFIG_PATH = Path.home() / ".config" / "bsky" / "config.json"


def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {}


def save_config(config):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2))
    os.chmod(CONFIG_PATH, 0o600)


def get_client():
    config = load_config()

    # Prefer session string (no password stored)
    if config.get("session"):
        client = Client()
        try:
            client.login(session_string=config["session"])
            # Update session in case it was refreshed
            new_session = client.export_session_string()
            if new_session != config["session"]:
                config["session"] = new_session
                save_config(config)
            return client
        except Exception:
            # Session expired/invalid, need to re-login
            print(
                "Session expired. Run: bsky login --handle your.handle --password your-app-password",
                file=sys.stderr,
            )
            sys.exit(1)

    # Legacy: support old configs with app_password (migrate on use)
    if config.get("handle") and config.get("app_password"):
        client = Client()
        client.login(config["handle"], config["app_password"])
        # Migrate to session-based auth
        config["session"] = client.export_session_string()
        del config["app_password"]
        save_config(config)
        print("(Migrated to session-based auth, app password removed)", file=sys.stderr)
        return client

    print(
        "Not logged in. Run: bsky login --handle your.handle --password your-app-password",
        file=sys.stderr,
    )
    sys.exit(1)


def cmd_login(args):
    try:
        client = Client()
        client.login(args.handle, args.password)
        # Store session string only - password never saved to disk
        config = {
            "handle": client.me.handle,
            "did": client.me.did,
            "session": client.export_session_string(),
        }
        save_config(config)
        print(f"Logged in as {client.me.handle} ({client.me.did})")
        print("(Password not stored - using session token)")
    except Exception as e:
        print(f"Login failed: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_logout(args):
    config = load_config()
    if config.get("session"):
        config.pop("session", None)
        config.pop("handle", None)
        config.pop("did", None)
        save_config(config)
        print("Logged out successfully")
    else:
        print("Not logged in")


def cmd_whoami(args):
    config = load_config()
    if config.get("handle"):
        client = get_client()
        print(f"Handle: {client.me.handle}")
        print(f"DID: {client.me.did}")
    else:
        print("Not logged in")


def cmd_timeline(args):
    from datetime import timezone, timedelta

    client = get_client()

    cutoff = None
    if getattr(args, "days", None):
        cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)

    fmt = getattr(args, "format", "text")
    json_out: list[dict] = []

    remaining = args.count
    cursor = None
    fetched = 0
    while remaining > 0:
        batch_limit = min(100, remaining)
        response = client.get_timeline(cursor=cursor, limit=batch_limit)
        if not response.feed:
            break

        batch_any_in_window = False
        for item in response.feed:
            post = item.post
            author = post.author.handle
            text = post.record.text if hasattr(post.record, "text") else ""
            created = post.record.created_at if hasattr(post.record, "created_at") else ""
            likes = post.like_count or 0
            reposts = post.repost_count or 0
            replies = post.reply_count or 0

            dt = None
            try:
                dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                time_str = dt.strftime("%b %d %H:%M")
            except Exception:
                time_str = created[:16] if created else ""

            if cutoff and dt and dt < cutoff:
                continue
            batch_any_in_window = True

            if fmt == "json":
                json_out.append(
                    {
                        "uri": post.uri,
                        "cid": getattr(post, "cid", None),
                        "author": {"handle": author, "did": getattr(post.author, "did", None)},
                        "record": {"text": text, "createdAt": created},
                        "created_at": created,
                        "likeCount": likes,
                        "repostCount": reposts,
                        "replyCount": replies,
                    }
                )
            else:
                print(f"@{author} · {time_str}")
                print(f"  {text[:200]}")
                print(f"  ❤️ {likes}  🔁 {reposts}  💬 {replies}")
                print(f"  🔗 https://bsky.app/profile/{author}/post/{post.uri.split('/')[-1]}")
                print()
            fetched += 1
            remaining -= 1
            if remaining <= 0:
                break

        if remaining <= 0:
            break
        if cutoff and not batch_any_in_window:
            break
        if not response.cursor:
            break
        cursor = response.cursor
        if fmt != "json":
            print(f"  ...fetched {fetched} posts, paging...", file=sys.stderr)

    if fmt == "json":
        print(json.dumps(json_out, default=str))


def cmd_post(args):
    text = args.text

    # Validate text
    if not text or not text.strip():
        print("Error: Post text cannot be empty", file=sys.stderr)
        sys.exit(1)

    if len(text) > 300:
        print(f"Error: Post is {len(text)} chars (max 300)", file=sys.stderr)
        sys.exit(1)

    # Dry run - show what would be posted without actually posting
    if args.dry_run:
        print("=== DRY RUN (not posting) ===")
        print(f"Text ({len(text)} chars):")
        print(f"  {text}")

        # Check for URLs
        url_pattern = r"(https?://[^\s]+)"
        urls = re.findall(url_pattern, text)
        if urls:
            print(f"Links detected: {len(urls)}")
            for url in urls:
                print(f"  • {url}")

        print("=============================")
        return

    client = get_client()

    # Auto-detect URLs and create proper facets using TextBuilder
    url_pattern = r"(https?://[^\s]+)"
    urls = re.findall(url_pattern, text)

    # Also detect @mentions
    mention_pattern = r"@([a-zA-Z0-9._-]+)"
    mentions = re.findall(mention_pattern, text)

    if urls or mentions:
        # Use TextBuilder for proper facets (links and mentions)
        builder = client_utils.TextBuilder()

        # Combined pattern to find both URLs and mentions in order
        combined_pattern = r"(https?://[^\s]+)|(@[a-zA-Z0-9._-]+)"
        last_end = 0

        # Resolve mention handles to DIDs
        mention_dids = {}
        for handle in mentions:
            full_handle = handle if "." in handle else f"{handle}.bsky.social"
            try:
                profile = client.get_profile(full_handle)
                mention_dids[handle] = profile.did
            except Exception:
                # If we can't resolve, skip making it a facet
                pass

        for match in re.finditer(combined_pattern, text):
            # Add text before the match
            if match.start() > last_end:
                builder.text(text[last_end : match.start()])

            if match.group(1):  # URL
                url = match.group(1)
                builder.link(url, url)
            elif match.group(2):  # Mention
                mention_text = match.group(2)
                handle = mention_text[1:]  # Remove @
                if handle in mention_dids:
                    builder.mention(mention_text, mention_dids[handle])
                else:
                    builder.text(mention_text)  # Can't resolve, just text

            last_end = match.end()

        # Add any remaining text
        if last_end < len(text):
            builder.text(text[last_end:])
        response = client.send_post(builder)
    else:
        response = client.send_post(text=text)

    uri = response.uri
    post_id = uri.split("/")[-1]
    print(f"Posted: https://bsky.app/profile/{client.me.handle}/post/{post_id}")


def cmd_delete(args):
    client = get_client()
    # Extract post ID from URL or use raw ID
    post_id = args.post_id
    if "bsky.app" in post_id:
        post_id = post_id.rstrip("/").split("/")[-1]

    # Construct the URI
    uri = f"at://{client.me.did}/app.bsky.feed.post/{post_id}"

    try:
        client.delete_post(uri)
        print(f"Deleted post: {post_id}")
    except Exception as e:
        print(f"Delete failed: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_profile(args):
    client = get_client()
    handle = args.handle.lstrip("@") if args.handle else client.me.handle

    # Auto-append .bsky.social if no domain specified
    if handle and "." not in handle:
        handle = f"{handle}.bsky.social"

    profile = client.get_profile(handle)
    print(f"@{profile.handle}")
    print(f"  Name: {profile.display_name or '(none)'}")
    print(f"  Bio: {profile.description or '(none)'}")
    print(f"  Followers: {profile.followers_count}")
    print(f"  Following: {profile.follows_count}")
    print(f"  Posts: {profile.posts_count}")
    print(f"  DID: {profile.did}")


def cmd_search(args):
    client = get_client()
    response = client.app.bsky.feed.search_posts({"q": args.query, "limit": args.count})

    if not response.posts:
        print("No results found.")
        return

    for post in response.posts:
        author = post.author.handle
        text = post.record.text if hasattr(post.record, "text") else ""
        likes = post.like_count or 0

        print(f"@{author}: {text[:150]}")
        print(
            f"  ❤️ {likes}  🔗 https://bsky.app/profile/{author}/post/{post.uri.split('/')[-1]}"
        )
        print()


def cmd_notifications(args):
    client = get_client()
    response = client.app.bsky.notification.list_notifications({"limit": args.count})

    fmt = getattr(args, "format", "text")
    if fmt == "json":
        out = []
        for notif in response.notifications:
            text = ""
            rec = getattr(notif, "record", None)
            if rec is not None and hasattr(rec, "text"):
                text = rec.text or ""
            out.append(
                {
                    "uri": getattr(notif, "uri", None),
                    "cid": getattr(notif, "cid", None),
                    "reason": notif.reason,
                    "author": {
                        "handle": notif.author.handle,
                        "did": getattr(notif.author, "did", None),
                    },
                    "record": {"text": text},
                    "indexedAt": notif.indexed_at,
                    "isRead": getattr(notif, "is_read", None),
                }
            )
        print(json.dumps(out, default=str))
        return

    for notif in response.notifications:
        reason = notif.reason
        author = notif.author.handle
        time_str = notif.indexed_at[:16] if notif.indexed_at else ""

        icons = {
            "like": "❤️",
            "repost": "🔁",
            "follow": "👤",
            "reply": "💬",
            "mention": "📢",
            "quote": "💭",
        }
        icon = icons.get(reason, "•")

        if reason == "like":
            print(f"{icon} @{author} liked your post · {time_str}")
        elif reason == "repost":
            print(f"{icon} @{author} reposted · {time_str}")
        elif reason == "follow":
            print(f"{icon} @{author} followed you · {time_str}")
        elif reason == "reply":
            print(f"{icon} @{author} replied · {time_str}")
        elif reason == "mention":
            print(f"{icon} @{author} mentioned you · {time_str}")
        elif reason == "quote":
            print(f"{icon} @{author} quoted you · {time_str}")
        else:
            print(f"{icon} {reason} from @{author} · {time_str}")


def cmd_archive(args):
    """Fetch a full post history for a given handle via public list_records.

    No auth required for reading - list_records is a public AT Protocol endpoint.
    If no handle is passed and the user is logged in, archive the logged-in user.
    """
    client = Client()

    handle = args.handle
    if handle:
        handle = handle.lstrip("@")
        if "." not in handle:
            handle = f"{handle}.bsky.social"
        # Public endpoint - no auth needed
        resolved = client.com.atproto.identity.resolve_handle(params={"handle": handle})
        did = resolved.did
    else:
        config = load_config()
        if not config.get("did") or not config.get("handle"):
            print(
                "No handle given and not logged in. Pass --handle or run `bsky login` first.",
                file=sys.stderr,
            )
            sys.exit(1)
        handle = config["handle"]
        did = config["did"]

    cursor = None
    posts = []
    while True:
        resp = client.com.atproto.repo.list_records(
            params={
                "repo": did,
                "collection": "app.bsky.feed.post",
                "limit": 100,
                "cursor": cursor,
            }
        )
        posts.extend(resp.records)
        print(f"  ...fetched {len(posts)} posts", file=sys.stderr)
        if not resp.cursor:
            break
        cursor = resp.cursor

    posts.sort(key=lambda r: getattr(r.value, "created_at", "") or "")

    if args.out:
        out_path = Path(args.out)
    else:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        out_path = Path.cwd() / f"bluesky-archive-{handle}-{today}.{args.format}"

    if args.format == "json":
        serialized = [
            {
                "uri": r.uri,
                "cid": r.cid,
                "value": r.value.model_dump(mode="json") if hasattr(r.value, "model_dump") else dict(r.value),
            }
            for r in posts
        ]
        out_path.write_text(
            json.dumps(
                {
                    "handle": handle,
                    "did": did,
                    "fetched_at": datetime.utcnow().isoformat() + "Z",
                    "count": len(posts),
                    "posts": serialized,
                },
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )
    else:  # markdown
        lines = [
            f"# Bluesky archive - @{handle}",
            "",
            f"Fetched: {datetime.utcnow().isoformat()}Z",
            f"Total posts: {len(posts)}",
            "",
        ]
        for rec in posts:
            r = rec.value
            rkey = rec.uri.split("/")[-1]
            text = getattr(r, "text", "") or ""
            created = getattr(r, "created_at", "") or ""
            reply_to = ""
            if getattr(r, "reply", None):
                try:
                    reply_to = r.reply.parent.uri
                except Exception:
                    reply_to = ""
            embed_kind = ""
            if getattr(r, "embed", None):
                embed_kind = type(r.embed).__name__
            url = f"https://bsky.app/profile/{handle}/post/{rkey}"
            lines.append(f"## {created}")
            lines.append(f"url: {url}")
            if reply_to:
                lines.append(f"reply_to: {reply_to}")
            if embed_kind:
                lines.append(f"embed: {embed_kind}")
            lines.append("")
            lines.append(text)
            lines.append("")
        out_path.write_text("\n".join(lines), encoding="utf-8")

    size = out_path.stat().st_size
    print(f"Wrote {out_path} ({len(posts)} posts, {size} bytes)")


def main():
    parser = argparse.ArgumentParser(description="Bluesky CLI")
    parser.add_argument("-v", "--version", action="version", version=f"bsky {VERSION}")
    subparsers = parser.add_subparsers(dest="command")

    # login
    login_p = subparsers.add_parser("login", help="Login to Bluesky")
    login_p.add_argument(
        "--handle", required=True, help="Your handle (e.g. user.bsky.social)"
    )
    login_p.add_argument(
        "--password", required=True, help="App password (not your main password)"
    )

    # logout
    subparsers.add_parser("logout", help="Log out and clear session")

    # whoami
    subparsers.add_parser("whoami", help="Show current user")

    # timeline
    tl_p = subparsers.add_parser(
        "timeline", aliases=["tl", "home"], help="Show home timeline"
    )
    tl_p.add_argument("-n", "--count", type=int, default=10, help="Max number of posts (paginates in batches of 100)")
    tl_p.add_argument("--days", type=int, help="Stop once posts older than this many days are reached")
    tl_p.add_argument("--format", choices=["text", "json"], default="text", help="Output format (default: text)")

    # post
    post_p = subparsers.add_parser("post", aliases=["p"], help="Create a post")
    post_p.add_argument("text", help="Post text")
    post_p.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be posted without posting",
    )

    # delete
    del_p = subparsers.add_parser("delete", aliases=["del", "rm"], help="Delete a post")
    del_p.add_argument("post_id", help="Post ID or URL")

    # profile
    profile_p = subparsers.add_parser("profile", help="Show profile")
    profile_p.add_argument(
        "handle", nargs="?", help="Handle to look up (default: self)"
    )

    # search
    search_p = subparsers.add_parser("search", aliases=["s"], help="Search posts")
    search_p.add_argument("query", help="Search query")
    search_p.add_argument(
        "-n", "--count", type=int, default=10, help="Number of results"
    )

    # notifications
    notif_p = subparsers.add_parser(
        "notifications", aliases=["notif", "n"], help="Show notifications"
    )
    notif_p.add_argument(
        "-n", "--count", type=int, default=20, help="Number of notifications"
    )
    notif_p.add_argument(
        "--format", choices=["text", "json"], default="text", help="Output format (default: text)"
    )

    # archive
    archive_p = subparsers.add_parser(
        "archive", help="Fetch full post history for a user (public, no auth)"
    )
    archive_p.add_argument(
        "--handle",
        help="Handle to archive (default: logged-in user)",
    )
    archive_p.add_argument(
        "--out",
        help="Output file path (default: ./bluesky-archive-<handle>-<date>.<format>)",
    )
    archive_p.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )

    args = parser.parse_args()

    commands = {
        "login": cmd_login,
        "logout": cmd_logout,
        "whoami": cmd_whoami,
        "timeline": cmd_timeline,
        "tl": cmd_timeline,
        "home": cmd_timeline,
        "post": cmd_post,
        "p": cmd_post,
        "delete": cmd_delete,
        "del": cmd_delete,
        "rm": cmd_delete,
        "profile": cmd_profile,
        "search": cmd_search,
        "s": cmd_search,
        "notifications": cmd_notifications,
        "notif": cmd_notifications,
        "n": cmd_notifications,
        "archive": cmd_archive,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
