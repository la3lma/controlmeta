
class MediaAndMetaStorage:

    def create_new_media_entry_from_metadata(self, metadata):
        returnValue= {
            "Name": "Test",
            "Latitude": 12.59817,
            "Longitude": 52.12873,
            "ContentURL": "http://server/media/id/21323",
            "ContentId": "21323"
            }
        return returnValue

    
    def post_media_to_id(self, id, mimetype, data):
        return {}

    def get_all_media(self):
        return []

    def drit(self):
        return "ja"

    def get_media(self, id):
        return "jalla"
        mimetype='text/plain'
        data='this is amazing'
        return mimetype, data


    
