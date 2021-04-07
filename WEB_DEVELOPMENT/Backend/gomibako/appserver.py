
#if __name__ == '__main__':
from server_app.app_server import app
from server_app.app_server import socketio
app = app
#app.run(host='0.0.0.0',use_reloader=False,debug=True)
socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)