from modal import Image, Stub, Secret, web_endpoint
from typing import Dict
from os import environ
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine

image = Image.debian_slim().apt_install("libpq-dev", "postgresql").pip_install("SQLAlchemy", "pandas", "psycopg2")
stub = Stub("hn_login_user", image = image)

@stub.function(secret = Secret.from_name("my-custom-secret"))
@web_endpoint(method = "POST")
def square(account_id):
    
    eng = create_engine(environ['HN_USER_DB'])
    name = pd.read_sql("SELECT user_name FROM users where account_id='{}'".format(account_id), con = eng).user_name.values[0]
    print(name)
    
    return {'name': name}
