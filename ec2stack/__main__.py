#!/usr/bin/env python
# encoding: utf-8

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

import ec2stack


def main():
    """


    """
    app = ec2stack.create_app()

    run_simple(
        app.config['EC2STACK_BIND_ADDRESS'],
        int(app.config['EC2STACK_PORT']),
        DispatcherMiddleware(app),
        use_reloader=True,
        use_debugger=True
    )


if __name__ == "__main__":
    main()
