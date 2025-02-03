from waitress import serve
from translator.wsgi import application

if __name__ == "__main__":
    serve(application, host="localhost", port='9000')