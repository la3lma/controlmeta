
class Entry:

    def __init__(self, id, content_type, content, metadata):
      self.id = id
      self.content_type = content_type
      self.content = content
      self.metadata = metadata

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
        object = Entry(
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

    # XXXX This is f-ed up.   Delete or fix
    def get_meta_list(self, id, metatype):
        # Empty map means no metadata found
        return {}

    def get_metadata_from_id(self, id, meta_id):
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
