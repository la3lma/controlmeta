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
    content = Column(String)
    meta_data = Column(String)

    def __init__(self,content_type, content, meta_data):
      self.content_type = content_type
      self.content = content
      self.meta_data = meta_data

class RDBMSMediaAndMetaStorage:

    def __init__(self, base_url):
        self.base_url = base_url

    def create_new_media_entry(self, mimetype, data):

        object = MediaMetaEntry(
            mimetype,
            data,
            None
            )

        db_session.add(object)


        # Set a couple of pieces of metadata that can't be
        # set by the setter
        # XXX The base URI is completely bogus
        meta_data = {}

        id = object.id
        url = ("%smedia/id/%s"%(self.base_url, id))
        meta_data['ContentURL']  = url
        meta_data['ContentId']  = id

        object.meta_data = json.dumps(meta_data)

        commit_db()
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
        commit_db()
        return {}

    def get_all_meta(self):
        keys = []
        for key in db_session.query(MediaMetaEntry.id):
            k = key[0]
            keys.append(k)
        return keys

    def get_media(self, id):
        id=str(id)
        result = db_session.query(MediaMetaEntry).get(id)
        if  result:
            return result.content_type, result.content
        else:
            return None, None

    def delete_media(self, id):
        id=str(id)
        ## XXX This is wasteful. We sholdn't have
        ##     to get the full object, we shuld just
        ##     nuke it from orbit.
        result = db_session.query(MediaMetaEntry).get(id)
        if result:
            db_session.delete(result)
            commit_db()
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


class MediaAndMetaStorage:

    def clear(self):
        self.objects = {}
        self.next_index = 1

    def __init__(self, base_url):
        self.base_url = base_url
        self.clear()

    def create_new_media_entry(self, mimetype, data):
        contentId = str(self.next_index)
        self.next_index = self.next_index + 1

        # Set a couple of pieces of metadata that can't be
        # set by the setter
        # XXX The base URI is completely bogus
        meta_data = {}
        url = ("%smedia/id/%s"%(self.base_url, contentId))
        meta_data['ContentURL']  = url
        meta_data['ContentId']  = contentId
        object = MediaMetaEntry(
            contentId,
            mimetype,
            data,
            meta_data)
        self.objects[contentId] = object
        return meta_data

    
    def post_media_to_id(self, id, mimetype, data):
        id=str(id)
        if id in self.objects:
            object = self.objects[id]
            object.content_type=mimetype
            object.content=data
        else:
            contentId = str(self.next_index)
            self.next_index = self.next_index + 1
            meta_data = {}
            object = MediaMetaEntry(
                contentId,
                mimetype,
                data,
                meta_data)
            self.objects[contentId] = object            
        return {}

    def get_all_meta(self):
        keys = self.objects.keys()
        return keys

    def get_media(self, id):
        id=str(id)
        if  id in self.objects:
            ob = self.objects.get(id)
            return ob.content_type, ob.content
        else:
            return None, None

    def delete_media(self, id):
        id=str(id)

        if (id in self.objects):
            del self.objects[id]
            ## Empty map means no errors
            
            return {}
        else:
            retval = {"Unknown_media_id": id}
            return retval

    def get_meta_list(self, id, metatype):
        # Empty map means no metadata found
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
