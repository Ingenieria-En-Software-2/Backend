from webapp import create_app

env = 'dev'
app = create_app('config.%sConfig' % env.capitalize())
 
# main driver function
if __name__ == "__main__":
    app.run()