from mcp.server.fastmcp import FastMCP

mcp = FastMCP("IGRAC GGIS")

import igrac_mcp.tools.wells  # noqa: E402, F401
import igrac_mcp.tools.measurements  # noqa: E402, F401
import igrac_mcp.tools.datasets  # noqa: E402, F401
import igrac_mcp.tools.statistic  # noqa: E402, F401
