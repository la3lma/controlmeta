from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import schema, types
from database import Base, db_session, commit_db
from sqlalchemy.orm import backref, relationship
from model_exception import ModelException

import json


class MediaEntry(Base):
    __tablename__ = 'media'

    id = schema.Column(Integer, primary_key=True)
    content_type = Column(String)
    content = Column(LargeBinary)
    metadatax  = relationship(
        "MetaEntry", 
        order_by="MetaEntry.id",
        backref='media_id',
        cascade="all, delete, delete-orphan")

    def __init__(self, content_type, content):
      self.content_type = content_type
      self.content = content

    def location_as_map(self, storage):
       return {
           "media_id": self.id, 
           "media_url": storage.get_media_url(self.id)
           }


class MetaEntry(Base):
    __tablename__ = 'meta'
    id = schema.Column(Integer, primary_key=True)
    mediaid  = Column(Integer, ForeignKey('media.id'))
    metatype = Column(String)
    content = Column(LargeBinary)

    # XXX This is supposed to be a one to one relationship between
    #     metadata (perhaps one to many) indicating that a piece of media
    #     relates to a piece of meta, and if the meta goes, so should
    #     the media.
    supplementing_relationship = relationship(
        "MediaEntry",
        single_parent=True,
        order_by="MediaEntry.id",
        backref='supplementing_meta_id',
        cascade="all, delete, delete-orphan")

    def __init__(self, mediaid,  metatype, content):
        self.mediaid = mediaid
        self.metatype = metatype
        self.content = content


    # XXX Rename the meta_type to be something else, such as "label"
    #     to emphasize that its not a media type for the meta content.
    def as_map(self, storage):
        return {
            'meta_id': self.id, 
            'media_id': self.mediaid, 
            'meta_type': self.metatype, 
            'meta_content': json.loads(self.content),
            'meta_url': storage.get_meta_url(self.id),
            'media_url': storage.get_media_url(self.mediaid)
         }


class RDBMSMediaAndMetaStorage:

    def __init__(self, base_url):

        if  base_url.endswith("/"):
            self.base_url = base_url
        else:
            self.base_url = base_url + "/"

    def get_media_url(self, id):
        return self.base_url + "media/id/" + str(id)

    def get_meta_url(self, id):
        return self.base_url + "media/metaid/" + str(id)


    def create_new_media_entry(self, mimetype, data):
        object = MediaEntry(
            mimetype,
            data)

        db_session.add(object)
        db_session.commit()

        if not object.id:
            raise ModelException("Null object.id  detected for MediaEntry", 500)

        return object.location_as_map(self)


    def post_media_to_id(self, id, mimetype, data):
        id=str(id)

        entry = db_session.query(MediaEntry).get(id)

        if entry:
            entry.content_type = mimetype
            entry.content = data
        else:
            error_msg ="Attempt to post media to nonexistant id " + id
            raise ModelException(error_msg, http_returnvalue = 404)
        return entry.location_as_map(self)

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
            raise ModelException("Cannot find media with id = " + id, 404)



    def delete_media(self, id):
        id=str(id)
        ## XXX This is wasteful. We sholdn't have
        ##     to get the full object, we shuld just
        ##     nuke it from orbit.
        result = db_session.query(MediaEntry).get(str(id))
        if result:
            db_session.delete(result)
        else:
            raise ModelException("Unknown media ID = " + str(id), 404)

        
    def store_new_meta_from_type(self, metatype, payload):
        meta_data = self.create_new_media_entry(None, None)
        media_id = meta_data['media_id']
        if not media_id:
            raise ModelException("Null media_id detected", 500)
        return self.store_new_meta(media_id, metatype, payload)


    def assert_that_media_id_exists(self, media_id):
        ret = db_session.query(exists().where(MediaEntry.id==media_id)).scalar()

        if not ret:
            raise ModelException("Unknown media ID " + media_id, 404)


    def store_new_meta_from_id_and_type(self, media_id, metatype, payload):
        "Store new meta from a type for an existing media entry."
        media_id = str(media_id)
        self.assert_that_media_id_exists(media_id)
        return self.store_new_meta(media_id,  metatype, payload)


    def store_new_meta(self, media_id, metatype, payload):
        if not media_id:
            raise ModelException("Null media_id detected", 500)

        json_payload = json.dumps(payload)

        entry = MetaEntry(media_id, metatype, json_payload)
        db_session.add(entry)
        db_session.commit()
        return entry.as_map(self)

                
    def basic_get_metadata_from_id(self, meta_id):
        meta_entry = db_session.query(MetaEntry).get(meta_id)
        if not meta_entry:
                raise ModelException(
                    "No metadata instance for object "
                    + ", with metaid = " 
                    + meta_id,
                    404)
        return meta_entry

    def update_meta_meta(self, meta_id, payload):
        meta_entry = self.basic_get_metadata_from_id(meta_id)
        meta_entry.content = payload


    def get_metadata_from_id(self,  meta_id):
        meta_entry = self.basic_get_metadata_from_id(meta_id)
        return_value = meta_entry.as_map(self)
        return return_value

    
    def get_metadata_from_id_and_metatype(self, media_id, meta_type):
        
        media_id = str(media_id)
        self.assert_that_media_id_exists(media_id)
        
        entries = db_session.query(MetaEntry).filter_by(
            mediaid = media_id, 
            metatype = meta_type).all()
        result = []
        for item in entries:
            result.append(item.as_map(self))
        return result


    def delete_meta_from_id(self, meta_id):
        "Empty map means that no data was deleted"
        result = db_session.query(MetaEntry).get(meta_id)
        if result:
            db_session.delete(result)
            return {}
        else:
            raise ModelException("Unknown meta_id" +  meta_id, 404)

    def clean(self):
        "Nuke everything"
        db_session.query(MetaEntry).delete()
        db_session.query(MediaEntry).delete()
        db_session.commit()
