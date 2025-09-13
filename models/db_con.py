from models.model import get_session
from sqlalchemy import select,func,text
from sqlalchemy.orm import joinedload
from threading import Thread
from datetime import *
import os,sys
import base64


def select_one(model, **filters):
    with get_session() as session:
        query = session.query(model)
        for key, value in filters.items():
            query = query.filter(getattr(model, key) == value)
        return query.first()

def select_all(model, **filters):
    with get_session() as session:
        query = session.query(model)
        if model.__name__ == "attanace": ###for any model
            query = query.options(joinedload(model.person))
        for key, value in filters.items():
            query = query.filter(getattr(model, key) == value)
        return query.all()

def insert_row(model, **kwargs):
    with get_session() as session:
        obj = model(**kwargs)
        session.add(obj)
        session.commit()
        return obj

def update_row(model, filters: dict, updates: dict):
    with get_session() as session:
        obj = session.query(model)
        for key, value in filters.items():
            obj = obj.filter(getattr(model, key) == value)
        obj = obj.first()
        if obj:
            for key, value in updates.items():
                setattr(obj, key, value)
            session.commit()
        return obj

def delete_row(model, **filters):
    with get_session() as session:
        obj = session.query(model)
        for key, value in filters.items():
            obj = obj.filter(getattr(model, key) == value)
        obj = obj.first()
        if obj:
            session.delete(obj)
            session.commit()
        return obj
def delete_all_rows(model):
    with get_session() as session:
        session.query(model).delete()
        session.commit()
    
def count_rows(model, column=None):
    with get_session() as session:
        if column is not None:
            return session.query(func.count(column)).scalar()
        else:
            return session.query(func.count()).select_from(model).scalar()
def all_table(dbs_name):
    with get_session() as session:
        if 'lite' ==dbs_name:
            result = session.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            table_names = [row[0] for row in result.fetchall()]
        elif 'my_sql' ==dbs_name:
            result = session.execute(text("SHOW TABLES;"))
            table_names = [row[0] for row in result.fetchall()]
        else:
            table_names = []
        return table_names