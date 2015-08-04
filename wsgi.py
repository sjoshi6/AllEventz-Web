from aye import app

aye_app = app.create_app('Prod')

if __name__ == '__main__':
    aye_app.run(host='0.0.0.0', port=9000)
