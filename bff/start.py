import uvicorn
from config.app_config import load_app_config, parse_arguments

if __name__ == "__main__":
    parser, args = parse_arguments()
    load_app_config()
    # import os
    # print(os.environ.items(), 'hehe')
    from config.logger import configure_logging
    configure_logging()
     
    uvicorn.run("server.main:app", host=args.host, port=args.port, reload=args.stage == "LOCAL")