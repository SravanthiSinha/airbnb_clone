from app import app
from config import HOST, PORT, DEBUG

'''this code will be executed only if this file is run directly and not from another file'''
if __name__ == '__main__':
    ''' Initializes the flask api server '''
    app.run(host=HOST, port=PORT, debug=DEBUG)
