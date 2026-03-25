---
name: recall
description: Use when the user explicitly wants to remember, find, or look up something from their saved spaces in Kepler — e.g. "find that article about X", "what did I save on Y", "do I have anything about Z". Do NOT use speculatively or for general research.
---

Interpret `$ARGUMENTS` as what the user wants to recall. If empty, ask the user what they're looking for before searching.

Use `mcp__kepler__search_links`.

If the user mentions a space, search within that scope when the tool supports it.

Present results as a memory retrieval — lead with what was found, include title, URL, and space. If multiple strong matches exist, list them. If nothing matches, say so plainly and suggest a different query or space.
