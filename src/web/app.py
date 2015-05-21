from flask import Flask, redirect, request, session, Response, render_template, abort
from message_streaming import event_stream, publish_message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'auie'

@app.route('/')
def home():
    try:
        user = session['user']
    except KeyError:
        return redirect('/login')
    else:
        return render_template('home.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            user = request.form['user']
        except KeyError:
            abort(400) # TODO: better error handling
        else:
            session['user'] = user
            return redirect('/')
    else:
        return app.send_static_file('login.html')

@app.route('/post', methods=['POST'])
def post_message():
    try:
        message = request.form['message']
    except KeyError:
        abort(400) # TODO: better error handling
    else:
        user = session.get('user', 'anonymous')
        publish_message(user, message)
        return Response(status=204)

@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True)
