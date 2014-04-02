
class MediaAndMetaStorage:

    media_objects = {}
    content_types = {}
    meta_objects = {}
    next_index = 1

    def create_new_media_entry_from_metadata(self, metadata):
        # We don't need no stinkin' locking!
        contentId = self.next_index
        self.next_index = self.next_index + 1
        metadata['ContentURL']  = "http://server/media/id/" +  `contentId`
        metadata['ConttentId']  = contentId
        self.meta_objects[contentId] = metadata
        return metadata
    
    def post_media_to_id(self, id, mimetype, data):
        self.media_objects[id] = data
        self.content_types[id] = mimetype
        return {}

    ## A bit uncertain about what this should return.   All metaobjects probably,
    ## or even better a sizable subset of them with instructions on how to get more if  required.
    def get_all_meta(self):
        return []

    def get_media(self, id):
        if  id in self.content_types:
            mimetype=self.content_types.get(id)
            data=self.media_objects.get(id)
            return mimetype, data
        else:
            return None, None


    def delete_media(self, id):
        self.media_objects.pop(id,  None)
        self.content_types.pop(id,  None)
        self.meta_objects.pop(id,  None)
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


    
