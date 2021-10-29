from CTF import create_app

app = create_app()

app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = 'upload/'

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="127.0.0.1", port=5000)