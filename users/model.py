from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import schema, types
from database import Base, db_session, commit_db
from sqlalchemy.orm import backref, relationship
from model_exception import ModelException

import json

## XXX
## Placeholder for an one-way hash function (deterministic).
## The encryption thingy should have a secret salt from somewhere, just to
## make it that much more difficult to guess what the hashes are going to be.
## Apart from that, just use SHA-1 or something, it's probably good enough.

def encrypt(arg):
    # XXX  Obviously something better is required
    return arg + "foo"


class EmailVerificationCode(Base):
    __tablename__ = 'email_verification_codes'
    id = schema.Column(Integer, primary_key=True)
    email_verification_code = Column(String)
    
    # XXX Missing date issued, date verified
    #     verification status, user being verified
    #     Once verification is complete, the verification code
    #     record should be nuked, so that we don't keep
    #     old records in the database.  It may be prudent
    #     to log it into some log (that is then put into
    #     redshift or something just to keep track of times from registration
    #     to verification), but it's not something we should keep track
    #     of here.

    def check_email_verification(self, email_verification_code):
        code_match = (self.email_verification_code == email_verifcation_code)
        # Check dates,  etc.
        return code_match
    
class UserEntry(Base):
    __tablename__ = 'user'

    id = schema.Column(Integer, primary_key=True)
    # XXX The API key should also be a primary key, but not one that
    #     is automatically generated.
    api_key = Column(String)
    hashed_api_secret  = Column(String)
    flickr_userid = Column(String)
    email_address = Column(String)
    # XXX Reference to email verification code is missing.
    #     Once the email is verified, we can just nuke it.
    email_verified = Column(Boolean)
    hashed_password = Column(String)

    def __init__(self, 
                 flickr_userid,
                 email_address):
        self.flickr_userid = flickr_userid
        self.email_address = email_address
        # XXX Create email verification code

    def set_password(self, clairtext_password):
        self.hashed_password =  encrypt(clairtext_password)

    def set_api_keys(self, api_key, hashed_api_secret):
        self.api_key = api_key
        self.hashed_api_secret = hashed_api_secret

    def check_password(self, clairtext_password):
        return self.hashed_password == encrypt(clairtext_password)

    def check_api_key(self, clairtext_api_key):
        return self.hashed_password == encrypt(clairtext_password)

    def as_map(self):
        return {
            "id" : self.id,
            "clairtext_user_id": self.clairtext_user_id,
            "flickr_userid":     self.flickr_userid,
            "email_address":     self.email_address
            }

class UserStorage:

    def __init__(self, base_url):
        if  base_url.endswith("/"):
            self.base_url = base_url
        else:
            self.base_url = base_url + "/"

    def get_user_url(self, id):
        return self.base_url + "media/user/" + str(id)

    # XXX BOgus
    def get_user_verification_url(self, id):
        return self.base_url + "media/user/" + str(id)


    def find_user_by_api_key(self, api_key):
        id=str(id)
        user = db_session.query(UserEntry.api_key == api_key).first()
        return user

    def new_unused_api_key(self):
        api_key = None
        while api_key and this.find_user_by_api_key(api_key):
            api_key = random_string(50)
        return api_key

    def new_api_keys(self, user_id):
        api_key = self.new_unused_api_key()
        hashed_api_secret = random_string(50)
        hashed_secret = encrypt(api_secret)
        user.set_api_keys(api_key, hashed_api_secret)
        return (api_key, api_secret)

###############
    # XXX  Move to helper class Can we move the existance, deletion (basically
    #      CRUD into a helper class, and thus compress the model classes somewhat?
    def check_and_return(user, checker, secret):
        if user and checker(secret):
            return user.as_map()
        else:
            return None

    def delete_by_id(self, the_class, explanation, id):
        id=str(id)
        result = db_session.query(the_class).get(str(id))
        if result:
            db_session.delete(result)
        else:
            raise ModelException(explanation + str(id), 404)
###############
        
    def verify_api_login(self, api_key, api_secret):
        user = self.find_user_by_api_key(api_key)
        return self.check_and_return(user, user.check_api_key, api_secret)

    def verify_user_login(email_address, clairtext_password):
        user = self.find_user_by_email_address(email_address)
        return self.check_and_return(user, user.check_password, clairtext_password)

    def create_new_user_entry(self, clairtext_user_id, hashed_secret_key):
        object = UserEntry() # XXXX Missing
        db_session.add(object)
        db_session.commit()

        return object.location_as_map(self)

    def exists_user(self, id):
        id=str(id)
        result = db_session.query(exists().where(UserEntry.id==id)).scalar()
        return result
    
    def delete_user(self, id):
        self.delete_by_id(UserEntry, "Unknown User id", id)

