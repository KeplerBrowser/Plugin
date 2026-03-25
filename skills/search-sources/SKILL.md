---
name: search-sources
description: Use when URLs have surfaced from tools or agents and the user may want related saved context from Kepler. Do NOT use for general research or when the user is explicitly trying to recall something — use the recall skill for that.
---

Kepler is a personal memory store for URLs. This skill is for contextual enrichment only: URLs are already on the table and you want to check whether the user has related saved context.

Derive the search query from the URLs or topic already present in the conversation — do not ask the user for a query.

Use `mcp__kepler__search_links`.

If the user specifies a space, search within that scope when the tool supports it.

Present results compactly: title, URL, and space. If nothing relevant matches, say so briefly.
