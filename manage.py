import os
import sys
from app import create_app, manager

# For Import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = create_app()


@manager.command
def run():
    app.run(port=5000)


if __name__ == "__main__":
    manager.run()
