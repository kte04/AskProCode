
# from app import app
from app.routes import *  # * includes app too


def main():
    app.run(debug=True, port=8080)


if __name__ == "__main__":
    main()
