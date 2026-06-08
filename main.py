from api import make

def main():
    app = make()
    app.run(
        host=app.config.get('API_HOST'),
        port=app.config.get('API_PORT'),
        debug=True
    )

if __name__ == '__main__':
    main()