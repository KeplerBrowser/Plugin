---
name: save-source
description: Save a URL or web resource to a Kepler space. Use when the user wants to bookmark, save, keep, file, or organize a source in their knowledge graph, including after a search or fetch turns up something worth storing.
---

Interpret `$ARGUMENTS` as the source the user wants to save to Kepler.

Use the `add_link` tool from the Kepler MCP server to save it.

If the user names a space, save it there.

If the user does not name a space, call the `list_spaces` tool from the Kepler MCP server and ask them to choose before saving.

Pass through any title, tags, notes, or other metadata the user explicitly provides when the tool supports it.

Confirm what was saved and which space it went to.
