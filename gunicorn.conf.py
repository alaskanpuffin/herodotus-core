import multiprocessing
import os

port = 8080
if os.environ.get('GUNICORN_PORT'):
    port = os.environ.get('GUNICORN_PORT')

bind = "0.0.0.0:" + str(port)
workers = multiprocessing.cpu_count() * 2 + 1