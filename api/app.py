from app import app
from config import HOST, PORT, DEBUG

if __name__ == '__main__':
    ''' Initializes the flask api server '''
    app.run(host=HOST, port=PORT, debug=DEBUG)
