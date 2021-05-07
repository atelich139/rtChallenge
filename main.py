from server import Server

if __name__ == '__main__':
    try:
        # TODO: Change this to uWSGI for production
        Server.app.run()
    except KeyboardInterrupt:
        pass
