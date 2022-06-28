from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:1234@pg_db:5432/kekw"

engine = create_engine(DATABASE_URL,
    echo=True
)

Base = declarative_base()

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine) 

