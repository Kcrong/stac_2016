from app import create_app, manager

app = create_app()


@manager.command
def run():
    app.run(port=5000)


if __name__ == "__main__":
    manager.run()
