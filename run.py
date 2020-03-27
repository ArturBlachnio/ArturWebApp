from awa import create_app
from awa.config import TestConfig

app = create_app(config_class=TestConfig)

if __name__ == '__main__':
    app.run(debug=True, host='192.168.2.11', port=5000)

