Flachat
=======

Flask chat application using Redis

Motivated project
------------------
* https://gist.github.com/pietern/348262
* https://github.com/jakubroztocil/chat
* https://github.com/steffenwt/nodejs-pub-sub-chat-demo

Install
-------

* Prerequiste

    Redis : http://redis.io/download

* Python library dependency

    pip install flask redis gevent gunicorn

Run
---
gunicorn --debug --worker-class=gevent -t 600 flachat:app -b 0.0.0.0:8000

