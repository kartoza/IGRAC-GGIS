from django.core.management.base import BaseCommand

from igrac_mcp.server import mcp


class Command(BaseCommand):
    help = 'Run the MCP server'

    def add_arguments(self, parser):
        parser.add_argument(
            '--transport',
            default='sse',
            choices=['stdio', 'sse', 'streamable-http'],
        )
        parser.add_argument('--host', default='0.0.0.0')
        parser.add_argument('--port', type=int, default=3006)

    def handle(self, *args, **options):
        mcp.settings.host = options['host']
        mcp.settings.port = options['port']
        mcp.run(transport=options['transport'])
