import os
import sys
import traceback
import click

from minions.server.mastersrver import server


class Log:
    def __init__(self):
        self.quiet = False
        self.traceback = False

    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info():
            message += os.linesep + traceback.format_exc().strip()
        click.echo(message)


log = Log()


@click.group()
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback


@main.command('run-server')
@click.option('--host', '-h', default="127.0.0.1", show_default='127.0.0.1', help="Host")
@click.option('--port', '-p', default="8000", show_default='8000', help="Port")
def run_server(host, port):
    server(host, port)


if __name__ == '__main__':
    try:
        main(prog_name='minions', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
