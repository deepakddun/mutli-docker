from server import app


if __name__ == "__main__":
    print("READY FOR CONNECTION")
    app.run(host="0.0.0.0",debug=True)