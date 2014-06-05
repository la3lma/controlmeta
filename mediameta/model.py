from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import schema, types
from database import Base, db_session, commit_db
import json

class ModelException(Exception):

    def __init__(self,  message, http_returnvalue = None):
        self.http_returnvalue = http_returnvalue
        self.message = message

    def __str__(self):
        return repr(self.message + " -> http code " + str(self.http_returnvalue))


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

    def get_initial_meta_data(self, id):
        url = ("%smedia/id/%s"%(self.base_url, id))

        return {"ContentURL": url,
                "ContentId": id,
                "nextId": 1,
                "content":{},
                "types":{}}

    def create_new_media_entry(self, mimetype, data):

        object = MediaMetaEntry(
            mimetype,
            data,
            None
            )

        db_session.add(object)

        # XXX If the commit fails, then we shouldn't return
        commit_db()

        meta_data = self.get_initial_meta_data(object.id)
        object.meta_data = json.dumps(meta_data)

        return meta_data


    def post_media_to_id(self, id, mimetype, data):
        id=str(id)

        entry = db_session.query(MediaMetaEntry).get(id)
        if entry:
            entry.content_type = mimetype
            entry.content = data
        else:
            error_msg ="Attempt to post media to nonexistant id " + id
            raise ModelException(error_msg, http_returnvalue = 404)
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

        
    def store_new_meta_from_type(self, metatype, payload):
        meta_data = self.create_new_media_entry(None, None)
        id = meta_data['ContentId']
        print "newly created id is = ", id
        return self.store_new_meta(id, meta_data, metatype, payload)


    def store_new_meta_from_id_and_type(self, id, metatype, payload):
        "Store new meta from a type for an existing media entry."
        id=str(id)

        metadata = self.get_metadata_from_id(id)
        if not metadata:
            raise ModelException("Unknown media ID " + id, 404)

        return self.store_new_meta(id, metadata, metatype, payload)

    def store_new_meta(self, id, metadata, metatype, payload):

        # Update next_id
        next_id = metadata['nextId']
        meta_id = next_id
        next_id += 1
        metadata['nextId'] = next_id

        # Remember the metatype this particular payload
        if not metatype in metadata['types']:
            metadata['types'][metatype] = [meta_id]
        else:
            metadata['types'][metatype].append(meta_id) 

        # Remember the actual payload
        metadata['content'][meta_id] = payload

        self.store_meta_data(id, metadata)

        return {"meta_id" : meta_id}

    def store_meta_data(self, id, metadata):
        meta_as_json =  json.dumps(metadata)

        db_session.query(MediaMetaEntry).\
                   filter(id==id).\
                   update({'meta_data': meta_as_json})


    def get_metadata_from_id(self, id):
        """Get the entire meta datastructure, as a map, for a particular ID. An empty
        map means that the datum does not exist and hence has no associated metadata 
        structure."""
        print "Finding metadata for id = ", id
        result = db_session.query(MediaMetaEntry, MediaMetaEntry.meta_data)\
            .filter(MediaMetaEntry.id == id).first()
        print "result -->", result
        if not result:
            return {}
        else:
            metadata = result.meta_data
            if not metadata:
                raise ModelException("No metadata found for id " + id,  404)
            
            metadata_json = json.loads(metadata)
            return metadata_json


    def get_metadata_from_id_and_metaid(self, id, metaid):
        # Empty map means no metadata found
        return {}


    def delete_metaid(self, id, metaid):
        # Empty map means that no data was deleted
        return {}


