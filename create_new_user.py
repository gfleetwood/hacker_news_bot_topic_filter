from modal import Image, Stub, Secret, web_endpoint
from typing import Dict
from os import environ
import pandas as pd
from io import StringIO
import random
import string
from sqlalchemy import create_engine

image = Image.debian_slim().apt_install("libpq-dev", "postgresql").pip_install("SQLAlchemy", "pandas", "psycopg2")
stub = Stub("hn_create_new_user", image = image)

@stub.function(secret = Secret.from_name("my-custom-secret"))
@web_endpoint(method = "POST")
def square(name):
    
    account_id = ''.join(random.choices(string.ascii_lowercase, k = 17))
    df = pd.DataFrame({"account_id": [account_id], "user_name": [name]})
    eng = create_engine(environ['HN_USER_DB'])
    df.to_sql("users", con = eng, index = False, if_exists = "append")
    
    return {'account_id': account_id}
