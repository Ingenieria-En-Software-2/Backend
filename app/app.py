from webapp import create_app
from dotenv import load_dotenv
from flask_cors import CORS


load_dotenv()  # load environment variables from .env file

env = "dev"
app = create_app("config.%sConfig" % env.capitalize())


CORS(app)  # for cross-origin requests for react dev server

# main driver function
if __name__ == "__main__":
    app.run()
