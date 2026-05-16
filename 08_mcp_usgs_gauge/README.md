# Exercise 8: Use MCP Servers to Download USGS Gauge Data

**Best practice:** Give Claude an MCP server with web access so it can query a live API, read the real response schema, and write correct parsing code — instead of writing code to call APIs it has never seen.

---

## Background: USGS Gauge Data

The USGS National Water Information System (NWIS) tracks thousands of stream gauges across the US. Its Instantaneous Values (IV) API returns 15-minute streamflow readings in JSON:

```
https://waterservices.usgs.gov/nwis/iv/?sites=06610000&parameterCd=00060&startDT=2023-06-01&endDT=2023-06-01&format=json
```

Key fields in the response:
- `value.timeSeries[0].variable.noDataValue` — sentinel for missing data (`-999999`)
- `value.timeSeries[0].values[0].value[]` — list of `{value, dateTime}` records
- `value.timeSeries[0].sourceInfo.siteName` — human-readable gauge name

Site `06610000` is the Missouri River at Omaha, NE — one of the most-studied gauges in the US.

---

## What you have

- `usgs_gauge.py` — four stub functions for fetching and processing NWIS data
- `test_usgs_gauge.py` — 12 tests covering parsing, flow statistics, and flood flagging
- `fixtures/nwis_response.json` — a real-format NWIS response with 5 hourly readings

---

## What is an MCP Server?

MCP (Model Context Protocol) lets you give Claude access to external tools — file systems, databases, web APIs — as first-class capabilities. When Claude has a **fetch** MCP server configured, it can make real HTTP requests during the conversation. This means Claude can:

1. Call the USGS API directly and read the actual JSON
2. Understand the exact schema from a live response
3. Write parsing code that matches the real structure
4. Verify its implementation against the tests you provide

Without the fetch MCP server, Claude has to guess at the API response format based on its training data, which may be outdated or imprecise.

### Setting up the fetch MCP server

The `mcp-server-fetch` package lets Claude make HTTP GET requests. Install it with:

```bash
pip install mcp-server-fetch
```

Then add it to Claude Code:

```bash
claude mcp add fetch -- python -m mcp_server_fetch
```

Or configure it in your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "fetch": {
      "command": "python",
      "args": ["-m", "mcp_server_fetch"]
    }
  }
}
```

Verify it is active with `/mcp` in Claude Code — you should see `fetch` listed.

---

## Exercise

### Part A — Without MCP (the guessing way)

Open Claude Code (no MCP server configured) and run:

```
implement the four stub functions in 08_mcp_usgs_gauge/usgs_gauge.py for site 06610000
then run python -m pytest 08_mcp_usgs_gauge/test_usgs_gauge.py -v
```

Observe: Claude writes `urllib` or `requests` code using guessed URL parameters and a reconstructed JSON schema. The `parse_nwis_response` function will likely get the nesting wrong (`timeSeries`, `values`, `value` is three levels deep), and the no-data sentinel check may be missing or use the wrong value. Tests will fail, and fixing them requires Claude to guess further.

### Part B — With MCP fetch server (the grounded way)

Make sure the fetch MCP server is configured (see above). Clear context with `/clear`, then try:

```
I need to implement four stub functions in usgs_gauge.py to retrieve and
process USGS streamflow data.

Before writing any code:
1. Use the fetch tool to call this URL and read the real response schema:
   https://waterservices.usgs.gov/nwis/iv/?sites=06610000&parameterCd=00060&startDT=2023-06-01&endDT=2023-06-01&format=json

2. Note the exact nesting path to the discharge values and the noDataValue field.

Then implement all four stubs in 08_mcp_usgs_gauge/usgs_gauge.py. After implementing, run:
   python -m pytest 08_mcp_usgs_gauge/test_usgs_gauge.py -v
All 12 tests must pass. Fix any failures before stopping.
```

Observe: Claude fetches the live API, reads the actual JSON structure, then writes `parse_nwis_response` with the correct three-level nesting and proper sentinel handling. The tests pass on the first or second attempt.

---

## What to notice

| | Without MCP | With MCP fetch |
|---|---|---|
| Schema knowledge | Claude guesses from training data | Claude reads the live response |
| Nesting accuracy | Often wrong (3 levels deep is easy to miss) | Correct — Claude can see it |
| No-data handling | May omit or use wrong sentinel value | Reads `noDataValue` from the response |
| Iteration needed | Multiple rounds of guessing and fixing | Usually passes on first attempt |

- The fetch MCP server does not write code — it gives Claude **evidence** to write better code
- The test fixture in `fixtures/nwis_response.json` uses the real NWIS format, so tests catch schema errors that would only surface at runtime otherwise
- This pattern generalizes to any REST API: give Claude fetch access, have it read the schema, then implement and test

---

## Check your starting state

All 12 tests should FAIL (stubs are not implemented — that is intentional):

```powershell
python -m pytest 08_mcp_usgs_gauge/test_usgs_gauge.py -v
```
