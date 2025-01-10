# from sqlalchemy import create_engine, Column, Integer, PrimaryKeyConstraint, String
# from pathlib import Path
# import  os
#
# from sqlalchemy.orm import  sessionmaker
# from sqlalchemy.ext.declarative import  declarative_base
#
# from db import database
#
# directory = Path.home()
# db = 'sqlite+pysqlite:///account_details'
#
# db_engine = create_engine(db,echo=True)
# try:
#     print(db)
#     connection = db_engine.connect()
# except Exception as e:
#     print(e)
#
# Base = declarative_base()
#
# class User(Base):
#     __tablename__ = 'users'
#
#     id = Column(Integer,primary_key=True,autoincrement=True)
#     name= Column(String(50),nullable=False)
#     email = Column(String(50),nullable=True)
#
# Base.metadata.create_all(bind=db_engine)
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
#
# database = SessionLocal()
#
# user_data = User(name="John",email="john@yopmail.com")
# database.add(user_data)
# database.commit()
# database.refresh(user_data)
# get_user = database.query(User).filter(User.id ==1).all()[0]
# print({"id":get_user.id,"name":get_user.name,"email":get_user.email})
# database.query(User).up