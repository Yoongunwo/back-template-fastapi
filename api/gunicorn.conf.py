# gunicorn.conf.py
bind = "0.0.0.0:8000"
worker_class = "uvicorn.workers.UvicornWorker" # workers = (2 * CPU cores) + 1 or workers = CPU cores (when I/O working a lot)
workers = 2
timeout = 120
keepalive = 60
max_requests = 10000
max_requests_jitter = 1000