import os
from webapp import create_app
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

load_dotenv()

env = 'dev'
app = create_app('config.%sConfig' % env.capitalize())
db = SQLAlchemy(app)  # ORM
migrate = Migrate()
migrate.init_app(app, db)

from model import User, Role

CORS(app)  # for cross-origin requests for react dev server

# main driver function
if __name__ == "__main__":
    app.run()
