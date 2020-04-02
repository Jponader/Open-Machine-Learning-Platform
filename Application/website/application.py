from app import app

application = app

if __name__ == "__main__":
	application.debug = True
	application.run(host="0.0.0.0", port=5000, debug=True)


