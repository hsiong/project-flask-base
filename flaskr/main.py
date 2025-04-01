from asgiref.wsgi import WsgiToAsgi
from uvicorn import Config, Server

from flaskr.route.recognition_routes import *
from flaskr.tool.flask_tool import create_app

if __name__ == '__main__':
    app, args = create_app()
    
    # 注册蓝图
    app.register_blueprint(api, url_prefix="/" + default_config.CONTEXT_PATH)
    
    # 转换 asgi
    asgi_app = WsgiToAsgi(app)
    
    # 启动服务 - 支持多线程
    print("Start server at 127.0.0.1:" + str(args.port) + "/" + default_config.CONTEXT_PATH)
    print()
    config = Config(app=asgi_app, host="0.0.0.0", port=args.port)
    server = Server(config)
    server.run()
