
class Entry:

    def __init__(self, id, content_type, content, metadata):
      self.id = id
      self.content_type = content_type
      self.content = content
      self.metadata = metadata

class MediaAndMetaStorage:

    objects = {}
    next_index = 1

    def create_new_media_entry_from_metadata(self, metadata):
        contentId = self.next_index
        self.next_index = self.next_index + 1

        # Set a couple of pieces of metadata that can't be
        # set by the setter
        metadata['ContentURL']  = "http://server/media/id/" +  `contentId`
        metadata['ConttentId']  = contentId
        object = Entry(
            contentId,
            None,
            None,
            metadata)
        self.objects[contentId] = object
        return metadata
    
    def post_media_to_id(self, id, mimetype, data):
        if id in self.objects:
            object = objects[id]
            object.content_type=mimetype
            object.content=data
        else:
            contentId = self.next_index
            self.next_index = self.next_index + 1
            metadata = {}
            object = Entry(
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
        if  id in self.objects:
            ob = objects.get(id)
            return ob.contenttype, ob.content
        else:
            return None, None

    def delete_media(self, id):
        self.objects.pop(id, None)
        ## Empty map means no errors
        return {}

    def get_meta_list(self, id, metatype):
        ## Empty map means no metadata found
        return {}

    def get_metadata_from_id(self, id, metaid):
        ## Empty map means no metadata found
        return {}

    def store_new_meta(self, id, metatype):
        ## Empty map means that no data was stored
        return {}


    def store_new_meta(self, id, metaid):
        ## Empty map means that no data was stored
        return {}


    def delete_metaid(self, id, metaid):
        ## Empty map means that no data was deleted
        return {}
