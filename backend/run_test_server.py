from app import app

if __name__ == '__main__':
    print("Starting test server on port 5001...")
    app.run(debug=True, host='0.0.0.0', port=5002)
