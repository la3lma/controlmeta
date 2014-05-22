from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import schema, types
from database import Base, db_session
import json

class MediaMetaEntry:
    __tablename__ = 'mediametaentry'

    id = schema.Column(Integer, primary_key=True)
    content_type = Column(String)
    content = Column(String)
    metadata = Column(String)

    def __init__(self, id, content_type, content, metadata):
      self.id = id
      self.content_type = content_type
      self.content = content
      self.metadata = metadata

class RDBMSMediaAndMetaStorage:

    def __init__(self, base_url):
        self.base_url = base_url

    def create_new_media_entry(self, mimetype, data):
        contentId = str(self.next_index)
        self.next_index = self.next_index + 1

        # Set a couple of pieces of metadata that can't be
        # set by the setter
        # XXX The base URI is completely bogus
        metadata = {}
        url = ("%smedia/id/%s"%(self.base_url, contentId))

        # XXX Stuff things into the metadata map
        #     Needs to be serialized to json before stuffing into
        #     database
        metadata['ContentURL']  = url
        metadata['ContentId']  = contentId

        object = MediaMetaEntry(
            contentId,
            mimetype,
            data,
            metadata)
        db_session.add(object)
        db_session.commit()
        return metadata

    def post_media_to_id(self, id, mimetype, data):
        id=str(id)

        entry = db_session.query(MediaMetaEntry).get(id)
        if entry:
            object.content_type=mimetype
            object.content=data
            # XXX Necessary or not?
            db_session.save(entry)
        else:
            contentId = str(self.next_index)
            self.next_index = self.next_index + 1
            metadata = {}
            object = MediaMetaEntry(
                contentId,
                mimetype,
                data,
                metadata)
            db_session.add(object)
        db_session.commit()
        return {}

    def get_all_meta(self):
        keys = []
        for key in db_session.query(MediaMetaEntry.id):
            keys.append(id)
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
            db_session.commit()
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
        metadata = {}
        url = ("%smedia/id/%s"%(self.base_url, contentId))
        metadata['ContentURL']  = url
        metadata['ContentId']  = contentId
        object = MediaMetaEntry(
            contentId,
            mimetype,
            data,
            metadata)
        self.objects[contentId] = object
        return metadata

    
    def post_media_to_id(self, id, mimetype, data):
        id=str(id)
        if id in self.objects:
            object = self.objects[id]
            object.content_type=mimetype
            object.content=data
        else:
            contentId = str(self.next_index)
            self.next_index = self.next_index + 1
            metadata = {}
            object = MediaMetaEntry(
                contentId,
                mimetype,
                data,
                metadata)
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
