Flachat
=======

Flask chat application with Redis



Install
-------

* Prerequiste

Redis : http://redis.io/download

* Python library dependency

pip install flask gevent gunicorn

Run
---
gunicorn --debug --worker-class=gevent -t 99999 flachat:app -b 0.0.0.0:8000
