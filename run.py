from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6174, debug=True)
    # to run the app ONLY in the default localhost:5000 or 127.0.0.1:5000, use line
    # app.run(debug=True)