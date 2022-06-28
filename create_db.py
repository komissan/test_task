from sql import Base, engine
from model import Item

print('Creating')

Base.metadata.create_all(engine)