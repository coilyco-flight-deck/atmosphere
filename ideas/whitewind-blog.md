# whitewind-blog

**What** - Kai already writes long-form (coilysiren.me). The Atmosphere angle is WhiteWind. Two open shapes, not yet decided:

- Port the blog to WhiteWind outright, so posts live as records in Kai's own atproto repo.
- Or keep coilysiren.me as the home and annotate it with WhiteWind, mirror or cross-post rather than migrate.

**Why it fits the Atmosphere** - WhiteWind blog posts are markdown records in your repo (`com.whtwnd.blog.entry`). Portable, and they ride the same atproto identity as everything else here.

**Open questions**

- Migrate vs mirror vs annotate. Mirror keeps the website repo as source of truth and is the low-risk start.
- Whether the existing `website` repo build can emit WhiteWind records as one more output target.

See [atproto-x-my-streams](atproto-x-my-streams.md) - the writing surface is where the platform-engineering and observability content would land.
