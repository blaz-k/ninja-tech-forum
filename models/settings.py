import os
import smartninja_redis
from sqla_wrapper import SQLAlchemy

redis = smartninja_redis.from_url(os.environ.get("REDIS_URL"))

db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)
