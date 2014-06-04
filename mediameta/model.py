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

    def get_initial_meta_data(self):
        return {"nextId": 1, "content":{}, "types":{}}

    def post_media_to_id(self, id, mimetype, data):
        id=str(id)

        entry = db_session.query(MediaMetaEntry).get(id)
        if entry:
            entry.content_type=mimetype
            entry.content=data
        else:
            meta_data = self.get_initial_meta_data()
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


    def store_new_meta_from_type(self, id, metatype, payload):
        "Store new meta from a type for an existing media entry."
        id=str(id)

        meta = self.get_metadata_from_id(id)

        # Update next_id
        next_id = meta['nextId']
        meta_id = next_id
        next_id += 1
        meta['nextId'] = next_id

        # Remember the metatype this particular payload
        if not metatype in meta['types']:
            meta['types'][metatype] = [meta_id]
        else:
            meta['types'][metatype].append(meta_id) 

        # Remember the actual payload
        meta['content'][meta_id] = payload

        # Persist the payload
        # XXX This thing does not work. db_session does not
        #     have an "update" method, so we'll have to 
        #     try something else.
        db_session.update(MediaMetaEntry).\
            where(MediaMetaEntry.id==id).\
            values(metadata = json.dump(meta))

        # Return id of this meta entry
        return meta_id


    def get_metadata_from_id(self, id):
        "Get the entire meta datastructure, as a map, for a particular ID"
        # XXX How to handle nulls?
        result = db_session.query(MediaMetaEntry, MediaMetaEntry.meta_data)\
            .filter(MediaMetaEntry.id == id).first()
        if not result:
            return {}
        else:
            metadata = result.meta_data
            print "get_meta.result = ", result
            metadata_json = json.loads(metadata)
            return metadata_json


    def get_metadata_from_id_and_metaid(self, id, metaid):
        # Empty map means no metadata found
        return {}


    def delete_metaid(self, id, metaid):
        # Empty map means that no data was deleted
        return {}


