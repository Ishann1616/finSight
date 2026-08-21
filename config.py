import os
SECRET_KEY =os.environ.get("SECRET_KEY","finsight-super-secret-key-change-in-production")
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DATABASE_URL= os.environ.get("DATABASE_URL","postgresql://postgres@localhost/finsight")
