from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import schema, types
from database import Base, db_session, commit_db
import json

class MediaMetaEntry(Base):
    __tablename__ = 'mediametaentry'

    id = schema.Column(Integer, primary_key=True)
    content_type = Column(String)
    content = Column(LargeBinary)
    meta_data = Column(String)

    def __init__(self,content_type, content, meta_data):
      self.content_type = content_type
      self.content = content
      self.meta_data = meta_data

class RDBMSMediaAndMetaStorage:

    def __init__(self, base_url):

        if  base_url.endswith("/"):
            self.base_url = base_url
        else:
            self.base_url = base_url + "/"

    def create_new_media_entry(self, mimetype, data):

        object = MediaMetaEntry(
            mimetype,
            data,
            None
            )

        db_session.add(object)

        # XXX IF the commit fails, then we shouldn't return
        commit_db()

        # Set a couple of pieces of metadata that can't be
        # set by the setter
        # XXX The base URI is completely bogus
        meta_data = {}

        id = object.id
        url = ("%smedia/id/%s"%(self.base_url, id))
        meta_data['ContentURL']  = url
        meta_data['ContentId']  = id

        object.meta_data = json.dumps(meta_data)

        return meta_data

    def post_media_to_id(self, id, mimetype, data):
        id=str(id)

        entry = db_session.query(MediaMetaEntry).get(id)
        if entry:
            entry.content_type=mimetype
            entry.content=data
        else:
            meta_data = {}
            entry = MediaMetaEntry(
                mimetype,
                data,
                json.dumps(meta_data))
            db_session.add(entry)
        return {}

    # XXX This is absolutely not scalable!!
    def get_all_media(self):
        keys = []
        for key in db_session.query(MediaMetaEntry.id):
            k = key[0]
            keys.append(k)
        return keys

    def get_media(self, id):
        id=str(id)
        result = db_session.query(MediaMetaEntry).get(id)
        if  result:
            return (result.content_type, result.content)
        else:
            return (None, None)

    def delete_media(self, id):
        id=str(id)
        ## XXX This is wasteful. We sholdn't have
        ##     to get the full object, we shuld just
        ##     nuke it from orbit.
        result = db_session.query(MediaMetaEntry).get(id)
        if result:
            db_session.delete(result)
            return {}
        else:
            retval = {"Unknown_media_id": id}
            return retval

    def get_meta_list(self, id, metatype):
        # Empty map means no meta_data found
        return {}

    def get_metadata_from_id(self, id, metaid):
        # Empty map means no metadata found
        return {}

    def store_new_meta(self, id, metatype):
        # Empty map means that no data was stored
        return {}

    def store_new_meta(self, id, metaid):
        # Empty map means that no data was stored
        return {}

    def delete_metaid(self, id, metaid):
        # Empty map means that no data was deleted
        return {}


