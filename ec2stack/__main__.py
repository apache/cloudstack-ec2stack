#!/usr/bin/env python
# encoding: utf-8

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

import ec2stack


def main():
    app = ec2stack.create_app()

    if 'EC2STACK_BIND_ADDRESS' in app.config:
        address = app.config['EC2STACK_BIND_ADDRESS']
    else:
        address = '0.0.0.0'

    if 'EC2STACK_PORT' in app.config:
        port = int(app.config['EC2STACK_PORT'])
    else:
        port = 5000

    run_simple(
        address,
        port,
        DispatcherMiddleware(app),
        use_reloader=True,
        use_debugger=True
    )


if __name__ == "__main__":
    main()
