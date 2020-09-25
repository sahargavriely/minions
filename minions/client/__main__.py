import click
import sys
import os
import traceback

from minions.client.client import upload_config, reset_server


class Log:

    def __init__(self):
        self.quiet = False
        self.traceback = False

    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info():  # there's an active exception
            message += os.linesep + traceback.format_exc().strip()
        click.echo(message)


log = Log()


@click.group()
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback


@main.command('upload-config')
@click.option('--host', '-h',
              default="127.0.0.1",
              show_default='127.0.0.1')
@click.option('--port', '-p',
              default="8000",
              show_default='8000')
@click.option('--hashedpassword', '-hp',
              default="0500000000",
              show_default='0500000000')
@click.argument('path')
def client_upload_config(host, port, hashedpassword, path):
    log(upload_config(host=host, port=port,
                      hashedpassword=hashedpassword, path=path))


@main.command('reset-server')
@click.option('--host', '-h', default="127.0.0.1", show_default='127.0.0.1', help="Host")
@click.option('--port', '-p', default="8000", show_default='8000', help="Port")
def client_reset_server(host, port):
    log(reset_server(host=host, port=port))


if __name__ == '__main__':
    try:
        main(prog_name='minions', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(42)
