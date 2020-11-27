if __name__ == '__main__':
    from server_app.app_server import app
    app.run(host='0.0.0.0',use_reloader=False,debug=True)