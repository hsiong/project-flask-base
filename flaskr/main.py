from gevent.pywsgi import WSGIServer

from flaskr.tool.flask_tool import create_app

from flaskr.route.recognition_routes import *


if __name__ == '__main__':
    
    app, args = create_app()
    
    # 注册蓝图
    app.register_blueprint(api, url_prefix="/" + default_config.CONTEXT_PATH_COW)
    
    # 启动服务 - 支持多线程
    print("Start server at 127.0.0.1:" + str(args.port) + "/" + default_config.CONTEXT_PATH)
    http_server = WSGIServer(("0.0.0.0", args.port), app) # 请确保 Flask 应用启动时监听的是 0.0.0.0，这样它可以从局域网内其他机器访问，而不仅仅是 localhost。
    http_server.serve_forever()