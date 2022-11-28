import main
import os


def create_app(envivorment=os.environ, start_response=None):
    return main.app
