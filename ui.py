#!/usr/bin/env python
import datetime
import flask
import redis

app = flask.Flask(__name__)
app.secret_key = 'auie'
red = redis.StrictRedis()

def event_stream():
    pubsub = red.pubsub()
    pubsub.subscribe('Anna')
    for message in pubsub.listen():
        print message
        yield 'data: %s\n\n' % message['data']

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        flask.session['user'] = flask.request.form['user']
        return flask.redirect('/')
    return '<form action="" method="post">user: <input name="user">'

@app.route('/post', methods=['POST'])
def post():
    message = flask.request.form['message']
    user = flask.session.get('user', 'anonymous')
    now = datetime.datetime.now().replace(microsecond=0).time()
    red.publish('Anna', u'[%s] %s: %s' % (now.isoformat(), user, message))
    return flask.Response(status=204)

@app.route('/stream')
def stream():
    return flask.Response(event_stream(), mimetype="text/event-stream")

@app.route('/')
def home():
    if 'user' not in flask.session:
        return flask.redirect('/login')
    return """
        <!doctype html>
        <title>Anna</title>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
        <style>body { max-width: 500px; margin: auto; padding: 1em; background: black; color: #fff; font: 16px/1.6 menlo, monospace; }</style>
        <table>
            <tr>
                <td colspan=2 align=center>
                    <h3> Anna's says </h3>
                </td>
                <td align=center>
                    <h3> Category </h3>
                </td>
            </tr>
            <tr>
                <td>
                    <p><b>hi, %s!</b></p>
                </td>
                <td colspan=2>
                    <br/>
                </td>
            </tr>
            <tr>
                <td>
                    <p>You say : <input id="in" /></p>
                    <pre id="out"></pre>
                </td>
                <td>
                &nbsp&nbsp&nbsp&nbsp
                </td>
                <td>
                    <select>
                        <option value="Action">Action</option>
                        <option value="Drama">Drama</option>
                        <option value="Comedy">Comedy</option>
                        <option value="Documentary">Documentary</option>
                    </select> 
                </td>
            </tr>
        </table>
        <script>
            function sse() {
                var source = new EventSource('/stream');
                var out = document.getElementById('out');
                source.onmessage = function(e) {
                    out.innerHTML =  e.data + '\\n' + out.innerHTML;
                };
            }
            $('#in').keyup(function(e){
                if (e.keyCode == 13) {
                    $.post('/post', {'message': $(this).val()});
                    $(this).val('');
                }
            });
            sse();
        </script>

    """ % flask.session['user']


if __name__ == '__main__':
    app.debug = True
    app.run()
