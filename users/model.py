from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import schema, types
from database import Base, db_session, commit_db
from sqlalchemy.orm import backref, relationship
from model_exception import ModelException
import string
import random
import json
import hashlib

def cryptohash(arg):
    return hashlib.sha256(arg).hexdigest()


lower_and_uppercase_characters = \
    string.ascii_uppercase + string.ascii_lowercase + string.digits

def random_string(size=50, chars=lower_and_uppercase_characters):
        return ''.join(random.choice(chars) for _ in range(size))


class UserVerification(Base):
    __tablename__ = 'user_verification_codes'
    id = schema.Column(Integer, primary_key=True)
    code = Column(String)

    def __init__(self, 
                 code):
        self.code  = code
    
    # XXX Missing date issued, date verified
    #     verification status, user being verified
    #     Once verification is complete, the verification code
    #     record should be nuked, so that we don't keep
    #     old records in the database.  It may be prudent
    #     to log it into some log (that is then put into
    #     redshift or something just to keep track of times from registration
    #     to verification), but it's not something we should keep track
    #     of here.

    def verify(self, code):
        result  = (self.code == code)
        #  XXX Check dates,  etc.
        return result
    
class UserEntry(Base):
    __tablename__ = 'user'

    id = schema.Column(Integer, primary_key=True)
    # XXX The API key should also be a primary key, but not one that
    #     is automatically generated.
    api_key = Column(String)
    hashed_api_secret  = Column(String)
    email_address = Column(String)
    # XXX Reference to email verification code is missing.
    #     Once the email is verified, we can just nuke it.
    verified = Column(Boolean)
    hashed_password = Column(String)

    def __init__(self, 
                 email_address):
        self.email_address = email_address
        # XXX Create user verification code

    def set_password(self, clairtext_password):
        self.hashed_password =  cryptohash(clairtext_password)

    def set_api_keys(self, api_key, clairtext_secret):
        self.api_key = api_key
        self.hashed_api_secret = cryptohash(clairtext_secret)


    def check_password(self, clairtext_password):
        cryptohashed_password = cryptohash(clairtext_password)
        retval = (self.hashed_password == cryptohashed_password)
        return retval


    def check_api_key(self, clairtext_api_secret):
        ekey = cryptohash(clairtext_api_secret)
        retval = (self.hashed_api_secret == ekey)
        return retval

    def as_map(self):
        return {
            "id" : self.id,
            "email_address":     self.email_address,
            "api_key":           self.api_key,
            "hashed_password":   self.hashed_password,
            "hashed_api_secret": self.hashed_api_secret # XXX Just for debuggingl
            }


    def __repr__(self):
        return "UserEntry(%r)"%self.as_map()

    def __str__(self):
        return self.__repr__()

class UserStorage:

    def __init__(self, base_url):
        if  base_url.endswith("/"):
            self.base_url = base_url
        else:
            self.base_url = base_url + "/"

    # XXX This shouldn't be necessary, but for some reason it is
    def clean(self):
        # Delete everything
        UserVerification.query.delete()
        UserEntry.query.delete()
        

    def get_user_url(self, id):
        return self.base_url + "user/" + str(id)

    def get_user_verification_url(self, secret):
        return self.base_url + "user/" + str(secret) + "/verification"

    def get_user_verification(self, code):
        secret = str(secret)
        verification = db_session.query(UserVerification.code == code).first()
        return verification

    def new_user(self, email):
        # XXX Check that the email isn't already used
        # XXX Actually, enforce that as a key restreaint int the data model
        user = UserEntry(email)
        db_session.add(user)
        return user


    # XXX This is a rather bogus method.
    def verify_user(self, code):
        vc = self.get_user_verification(code)
        if not vc:
            return False # XXX Throw exception?
        elif not vc.verify(code):
            return False # Throw exception?
        else:
            self.verified = true


    # XXX Why not just use .all()?
    def find_all_users(self):
        users = []
        for u in db_session.query(UserEntry):
            users.append(u)
        return users

    def find_user_by_api_key(self, api_key):
        api_key = str(api_key)
        user = db_session.query(UserEntry).filter(UserEntry.api_key == api_key).first()
        return user

    def find_user_by_id(self, id):
        id = str(id)
        user = db_session.query(UserEntry).filter(UserEntry.id == id).first()
        return user

    def find_user_by_email(self, email):
        email = str(email)
        user = db_session.query(UserEntry).filter(UserEntry.email_address == email).first()
        return user
    

    def new_unused_api_key(self):
        api_key = None
        while not api_key or self.find_user_by_api_key(api_key):
            api_key = random_string(50)
        return api_key

    def new_api_keys(self, user):
        api_key = self.new_unused_api_key()
        api_secret = random_string(50)
        user.set_api_keys(api_key, api_secret)
        return (api_key, api_secret)

###############
    # XXX  Move to helper class Can we move the existance, deletion (basically
    #      CRUD into a helper class, and thus compress the model classes somewhat?
    # XXX  This is dubious design!

    def check_and_return(self, user, checker, secret):
        if user and checker(secret):
            return user
        else:
            return None

    def delete_by_id(self, the_class, explanation, id):
        id=str(id)
        result = db_session.query(the_class).get(str(id))
        if result:
            db_session.delete(result)
        else:
            raise ModelException(explanation + " " + str(id), 404)
###############
        
    def verify_api_login(self, api_key, api_secret):
        user = self.find_user_by_api_key(api_key)
        if not user:
            return None
        else: 
            return self.check_and_return(user, user.check_api_key, api_secret)

    def verify_user_login(self, email_address, clairtext_password):
        user = self.find_user_by_email(email_address)
        if  not user:
            return None
        else:
            return self.check_and_return(user, user.check_password, clairtext_password)

    def exists_user(self, id):
        id=str(id)
        result = db_session.query(exists().where(UserEntry.id==id)).scalar()
        return result
    
    def delete_user(self, id):
        self.delete_by_id(UserEntry, "Unknown User id", id)

