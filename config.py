#  holds all configuration variables for this application here
#  should not be uploaded to github with sensetive information
# .gitignore this file
#  when uploading to heroku, use import as .get() method
import os

# define the root/base of this project folder
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # secret key is necessary for forms in flask, it is a security measure to protect against attacks like CSRF
    # it should never be given out, and should be something that is difficult to break
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    STRIPE_SECRET_KEY = 'sk_test_hZrdgq5APkXTMmTC1GyL6OJf'

    # setup database URI, which is the location of our database file/server
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(BASEDIR, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SQLALCHEMY_DATABASE_URI = 'postgressql://<admin>:<password>@<ip_address>:<port_number>/<server_name>'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'postgresql://postgres:Th7nkSeVeN!@localhost:5432/ecommerce'
