# IGRAC GGIS — AI Assistant Integration

## What is MCP?

**MCP (Model Context Protocol)** is a technology that connects AI assistants — such as Claude — directly to live databases and systems. Rather than manually searching through a platform, users can simply ask questions in plain language and receive instant, accurate answers drawn from real data.

Think of it as giving your AI assistant direct access to IGRAC GGIS, so it can look things up, filter results, and explain findings — all within a natural conversation.

**Example:**
> *"Show me all groundwater wells in the Netherlands with measurements from 2020 to 2026"*

The AI handles the query, retrieves the data, and presents a clear summary — no technical knowledge required.

---

## What Can It Do?

The IGRAC GGIS AI integration allows users to explore groundwater data conversationally:

- **Find wells** — search and filter wells by country, organisation, or identifier across the entire global database
- **Explore measurements** — retrieve water level, quality, and yield readings for any well, with optional date range and value filters
- **Browse datasets** — discover and inspect published GeoNode datasets, including their spatial coverage and available formats

---

## Examples

### Finding Wells Globally

A simple request to list wells returns the full inventory with location and elevation data — **149,597 wells** worldwide, paginated and easy to explore.

![List all wells](1-well-list.png)

---

### Filtering by Country

Asking for wells in a specific country instantly narrows the results. Here, filtering for the **Netherlands** returns **3,080 wells** from the Dutch groundwater monitoring network.

![Wells in the Netherlands](2-well-netherland.png)

---

### Checking Water Level Measurements

For any well, the AI can pull up its full measurement history. Well **GLD000000000004** has **67,850 hourly level readings**, with the most recent showing 11.708 m.

![Level measurements for GLD000000000004](3-level-measurement-GLD000000000004.png)

---

### Querying a Specific Time Period

Users can ask how much data exists within a date range. For the same well, there are **59,985 measurements between 2020 and 2026** — answered in seconds without opening any report or spreadsheet.

![Measurement count 2020–2026](4-level-measurement-GLD000000000004.png)

---

## Open API for GWML2 GGIS

Alongside the AI integration, we are also developing a **public Open API** for IGRAC GGIS. This will allow developers, researchers, and partner organisations to access groundwater data programmatically — directly from their own applications, scripts, or dashboards — without going through the web interface.



---

## What We Plan to Build Next

This integration is in its early stages. The following capabilities are on the roadmap:

### Deeper Data Access
- Full well profiles — drilling history, geology, aquifer type, and construction details
- Cross-country and regional comparisons in a single query
- Spatial search — find all wells within a geographic area

### Smarter Queries
- Trend detection — automatically identify wells with rising or declining water levels
- Anomaly alerts — flag unusual readings without manual inspection
- Summary reports — generate a country overview on demand

### Broader Dataset Support
- Access to all published GeoNode datasets, including maps and spatial layers
- Download links and OGC service connections surfaced through conversation

### Easier Access for Everyone
- Natural language queries that chain multiple steps automatically
- No login or technical setup required for read-only exploration
- Potential integration with web portals and reporting workflows