# -*- coding: utf-8 -*-
"""
    flachat
    ~~~~~~~~~~~~~
    comment:

    :copyright: (c) 2014 by liks. ( Jou Sung Shik, liks79 __at__ gmail.com )
    :license: MIT LICENSE 2.0 (http://opensource.org/licenses/MIT).
"""

from flask import Flask, render_template, request, session, Response, redirect, url_for
import datetime
import redis


app = Flask(__name__)
app.secret_key = 'flachat_secret'

r = redis.Redis(host='127.0.0.1', port=6379)
channel_name = 'chat:flask'


def event_stream():
    pubsub = r.pubsub()
    pubsub.subscribe(channel_name)

    for message in pubsub.listen():
        print message
        yield 'data: %s\n\n' % message['data']


def users_cnt():
    cnt = r.execute_command('PUBSUB', 'NUMSUB', channel_name)
    return cnt[1]


@app.route('/stream')
def stream():
    res = Response(event_stream(), mimetype='text/event-stream')
    res.headers.add('Cache-Control', 'no-cache')
    return res


@app.route('/logout')
def logout():
    pubsub = r.pubsub()
    pubsub.unsubscribe(channel_name)
    session.clear()

    return redirect(url_for('index'))


@app.route('/send', methods=['POST'])
def send():
    nick = session['nickname']
    message = request.form['message']

    now = datetime.datetime.now().replace(microsecond=0).time()
    r.publish(channel_name, u'[%s] %s: %s' % (now.isoformat(), nick, message))

    return Response(status=204)


@app.route('/')
def index():
    return render_template('index.html', users_cnt=users_cnt)


@app.route('/chat', methods=['GET', 'POST'])
def chat():

    if request.method == 'POST':
        session['nickname'] = request.form['nickname']
        session['logged_in'] = True
        res = render_template('chat.html', users_cnt=users_cnt)
    else:
        res = redirect('/')

    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)