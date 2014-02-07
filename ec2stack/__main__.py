#!/usr/bin/env python
# encoding: utf-8

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

import ec2stack


def main():
    app = ec2stack.create_app()

    address = app.config['EC2STACK_HOST'] if 'EC2STACK_HOST' in app.config \
        else '0.0.0.0'

    port = int(app.config['EC2STACK_PORT']) if 'EC2STACK_PORT' in app.config \
        else 5000

    run_simple(
        address,
        port,
        DispatcherMiddleware(app),
        use_reloader=True,
        use_debugger=True
    )


if __name__ == "__main__":
    main()
