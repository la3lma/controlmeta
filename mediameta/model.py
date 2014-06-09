from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import schema, types
from database import Base, db_session, commit_db
from sqlalchemy.orm import backref, relationship

import json

class ModelException(Exception):

    def __init__(self,  message, http_returnvalue = None):
        self.http_returnvalue = http_returnvalue
        self.message = message

    def __str__(self):
        return repr(self.message + " -> http code " + str(self.http_returnvalue))


class MediaEntry(Base):
    __tablename__ = 'media'

    id = schema.Column(Integer, primary_key=True)
    content_type = Column(String)
    content = Column(LargeBinary)
    meta_data  = relationship(
        "meta_data", 
        backref='media',
        cascade="all, delete, delete-orphan")

    def __init__(self,content_type, content):
      self.content_type = content_type
      self.content = content


class MetaEntry(Base):
    __tablename__ = 'meta'
    id = schema.Column(Integer, primary_key=True)
    meta_type = Column(String)
    content = Column(LargeBinary)
    media  = Column(Integer, ForeignKey('media.id'))

    def __init(self, media, meta_type, content):
        self.meta_type = meta_type
        self.content = content
        self.media = media

    def as_map():
        return {
            'meta_id': id, 
            'media_id': media, 
            'meta_type': meta_type, 
            'content': json.dumps(content)
         }


class RDBMSMediaAndMetaStorage:

    def __init__(self, base_url):

        if  base_url.endswith("/"):
            self.base_url = base_url
        else:
            self.base_url = base_url + "/"

    def create_new_media_entry(self, mimetype, data):

        object = MediaEntry(
            mimetype,
            data)

        db_session.add(object)
        return meta_data

    def post_media_to_id(self, id, mimetype, data):
        id=str(id)

        entry = db_session.query(MediaEntry).get(id)

        if entry:
            entry.content_type = mimetype
            entry.content = data
        else:
            error_msg ="Attempt to post media to nonexistant id " + id
            raise ModelException(error_msg, http_returnvalue = 404)
        return {}

    def get_all_media(self):
        keys = []
        for key in db_session.query(MediaEntry.id):
            k = key[0]
            keys.append(k)
        return keys

    def get_media(self, id):
        id=str(id)
        result = db_session.query(MediaEntry).get(id)
        if  result:
            return (result.content_type, result.content)
        else:
            return (None, None)

    def delete_media(self, id):
        id=str(id)
        ## XXX This is wasteful. We sholdn't have
        ##     to get the full object, we shuld just
        ##     nuke it from orbit.
        result = db_session.query(MediaEntry).get(id)
        if result:
            db_session.delete(result)
            return {}
        else:
            retval = {"Unknown_media_id": id}
            return retval
        
    def store_new_meta_from_type(self, metatype, payload):
        meta_data = self.create_new_media_entry(None, None)
        id = meta_data['ContentId']
        return self.store_new_meta(id, meta_data, metatype, payload)


    def store_new_meta_from_id_and_type(self, id, metatype, payload):
        "Store new meta from a type for an existing media entry."
        id=str(id)

        metadata = self.get_metadata_from_id(id)
        if not metadata:
            raise ModelException("Unknown media ID " + id, 404)

        return self.store_new_meta(id, metadata, metatype, payload)


    def store_new_meta(self, id, metadata, metatype, payload):

        entry = MetaEntry(id, metatype, payload)
        db_session.add(entry)
        db_session.commit()
        return {"meta_id" : entry.id, "ContentId": id}

    def get_metadata_from_metaid(self,  metaid):
        meta_data = self.get_metadata_from_id(str(id))
        if not meta_data:
                raise ModelException(
                    "No metadata instance for object "
                    + id 
                    + ", with metaid  " 
                    + metaid, 
                    404)
        
        return_value = meta_data.as_map()
        return return_value

    
    def get_metadata_from_id_and_metatype(self, media_id, metatype):
        entries = db_session.query(MetaEntry).filter_by(
            media = media_id, 
            meta_type = meta_type).all()
        # XXX Get all of them
        return []

    # XXX Placeholder
    def delete_metaid(self, meta_id):
        # Empty map means that no data was deleted
        result = db_session.query(MetaEntry).get(meta_id)
        if result:
            db_session.delete(result)
            return {}
        else:
            retval = {"Unknown_meta_id": meta_id}
            return retval


