# coding=utf-8
"""MCP (Model Context Protocol) settings."""

import os
from .prod import *  # noqa

INSTALLED_APPS += ('igrac_mcp',)  # noqa

MCP_SERVER_NAME = os.environ.get('MCP_SERVER_NAME', 'IGRAC GGIS')
MCP_SERVER_HOST = os.environ.get('MCP_SERVER_HOST', '0.0.0.0')
MCP_SERVER_PORT = int(os.environ.get('MCP_SERVER_PORT', '8001'))
