from app import app as application

if __name__ == "__main__":
	application.debug = True
	application.run(host="0.0.0.0", port=5001, debug=True)


