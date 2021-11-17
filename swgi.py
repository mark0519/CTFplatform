from CTF import create_app
import os

app = create_app()

app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = 'upload/'

if __name__ == "__main__":
    app.run()
