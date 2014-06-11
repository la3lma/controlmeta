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
    metadatax  = relationship(
        "MetaEntry", 
        order_by="MetaEntry.id",
#       backref='media_id',
        cascade="all, delete, delete-orphan")

    def __init__(self, content_type, content):
      self.content_type = content_type
      self.content = content


class MetaEntry(Base):
    __tablename__ = 'meta'
    id = schema.Column(Integer, primary_key=True)
    mediaid  = Column(Integer, ForeignKey('media.id'))
    metatype = Column(String)
    content = Column(LargeBinary)


    def __init__(self, mediaid,  metatype, content):
        self.mediaid = mediaid
        self.metatype = metatype
        self.content = content

    def get_url(self, id):
        return self.base_url + "media/metaid/" + str(id)


    def as_map(self):
        return {
            'meta_id': self.id, 
            'media_id': self.mediaid, 
            'meta_type': self.metatype, 
            'content': json.loads(self.content),
# XXX This should ge here, but the get_url screws up 
#     due to the base_url problem.
#            'URL': self.get_url(self.id)
         }


class RDBMSMediaAndMetaStorage:

    def __init__(self, base_url):

        if  base_url.endswith("/"):
            self.base_url = base_url
        else:
            self.base_url = base_url + "/"

    def get_url(self, id):
        return self.base_url + "media/id/" + str(id)

    def create_new_media_entry(self, mimetype, data):

        object = MediaEntry(
            mimetype,
            data)

        db_session.add(object)
        db_session.commit()

        if not object.id:
            raise ModelException("Null object.id  detected for MediaEntry", 500)
        

        # XXX Get the representation from the object itself, not from
        #     this ad-hoc thing.
        return {"ContentId": object.id, "ContentURL": self.get_url(object.id)}

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
        media_id = meta_data['ContentId']
        if not media_id:
            raise ModelException("Null media_id detected", 500)
        return self.store_new_meta(media_id, metatype, payload)


    def store_new_meta_from_id_and_type(self, media_id, metatype, payload):
        "Store new meta from a type for an existing media entry."
        media_id = str(media_id)

        ret = db_session.query(exists().where(MediaEntry.id==media_id)).scalar()

        if not ret:
            raise ModelException("Unknown media ID " + media_id, 404)

        return self.store_new_meta(media_id,  metatype, payload)


    def store_new_meta(self, media_id, metatype, payload):
        if not media_id:
            raise ModelException("Null media_id detected", 500)

        json_payload = json.dumps(payload)


        entry = MetaEntry(media_id, metatype, json_payload)
        db_session.add(entry)
        db_session.commit()
        return {"meta_id" : entry.id, "ContentId": media_id}

    def get_metadata_from_metaid(self,  metaid):
        meta_entry = db_session.query(MetaEntry).get(metaid)
        if not meta_entry:
                raise ModelException(
                    "No metadata instance for object "
                    + ", with metaid = " 
                    + metaid, 
                    404)
        
        return_value = meta_entry.as_map()
        return return_value

    
    def get_metadata_from_id_and_metatype(self, media_id, meta_type):
        entries = db_session.query(MetaEntry).filter_by(
            mediaid = media_id, 
            metatype = meta_type).all()
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
            raise ModelException("Unknown meta_id" +  meta_id, 404)




