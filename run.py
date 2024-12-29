
# from app import my_app
from app.routes import *  # * includes my_app too


def main():
    my_app.run(debug=True, port=8080)


if __name__ == "__main__":
    main()
