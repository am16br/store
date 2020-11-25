SECRET_KEY = os.urandom (256)
SQLALCHEMY_TRACK_MODIFICATIONS = False


# GCP
CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = 'paab6231'
CLOUDSQL_DATABASE = 'flaskr'
CLOUDSQL_CONNECTION_NAME = 'dumblit:us-east1:dumblit'
LOCAL_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{nam}:{pas}@127.0.0.1:3306/{dbn}').format (
    nam=CLOUDSQL_USER,
    pas=CLOUDSQL_PASSWORD,
    dbn=CLOUDSQL_DATABASE,
)

LIVE_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{nam}:{pas}@localhost/{dbn}?unix_socket=/cloudsql/{con}').format (
    nam=CLOUDSQL_USER,
    pas=CLOUDSQL_PASSWORD,
    dbn=CLOUDSQL_DATABASE,
    con=CLOUDSQL_CONNECTION_NAME,
)

if os.environ.get ('GAE_INSTANCE'):
    SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
else:
    SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI

# Override to SQLITE (for testing ...)
# SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
