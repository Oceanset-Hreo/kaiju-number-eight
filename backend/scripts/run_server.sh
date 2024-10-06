#!/bin/sh

# Run the server
gunicorn -c ./gunicorn/gunicorn.config.py wsgi:app
