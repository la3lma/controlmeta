from sqlalchemy import *
from sqlalchemy import schema
from database import Base, db_session
from model_exception import ModelException
import string
import random
import hashlib


def crypto_hash(arg):
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
        self.code = code

    # XXX Missing date issued, date verified
    # verification status, user being verified
    # Once verification is complete, the verification code
    # record should be nuked, so that we don't keep
    #     old records in the database.  It may be prudent
    #     to log it into some log (that is then put into
    #     redshift or something just to keep track of times from registration
    #     to verification), but it's not something we should keep track
    #     of here.

    def verify(self, code):
        result = (self.code == code)
        #  XXX Check dates,  etc.
        return result


class UserEntry(Base):
    __tablename__ = 'user'

    id = schema.Column(Integer, primary_key=True)
    # XXX The API key should also be a primary key, but not one that
    # is automatically generated.
    api_key = Column(String)
    hashed_api_secret = Column(String)
    email_address = Column(String)
    # XXX Reference to email verification code is missing.
    # Once the email is verified, we can just nuke it.
    verified = Column(Boolean)
    hashed_password = Column(String)

    def __init__(self,
                 email_address):
        self.email_address = email_address
        # XXX Create user verification code

    def set_password(self, clairtext_password):
        self.hashed_password = crypto_hash(clairtext_password)

    def set_api_keys(self, api_key, clairtext_secret):
        self.api_key = api_key
        self.hashed_api_secret = crypto_hash(clairtext_secret)

    def check_password(self, clair_text_password):
        cryptohashed_password = crypto_hash(clair_text_password)
        return_value = (self.hashed_password == cryptohashed_password)
        return return_value

    def check_api_key(self, clairtext_api_secret):
        cryptohashed_api_secret = crypto_hash(clairtext_api_secret)
        return_value = (self.hashed_api_secret == cryptohashed_api_secret)
        return return_value

    def as_map(self):
        return {
            "id": self.id,
            "email_address": self.email_address,
            "api_key": self.api_key,
            "hashed_password": self.hashed_password,
            "hashed_api_secret": self.hashed_api_secret  # XXX Just for debuggingl
        }

    def force_verified(self):
        self.verified = True

    def __repr__(self):
        return "UserEntry(%r)" % self.as_map()

    def __str__(self):
        return self.__repr__()


class UserStorage:
    def __init__(self, base_url):
        if base_url.endswith("/"):
            self.base_url = base_url
        else:
            self.base_url = base_url + "/"

    # XXX This shouldn't be necessary, but for some reason it is
    @staticmethod
    def clean():
        # Delete everything
        UserVerification.query.delete()
        UserEntry.query.delete()

    def report(self):
        pass

    def check_auth(self, email, password):
        user = self.find_user_by_email(email)
        if not user:
            return False
        else:
            return user.check_password(password)

    def get_user_url(self, user_id):
        return self.base_url + "user/" + str(user_id)

    def get_user_verification_url(self, secret):
        return self.base_url + "user/" + str(secret) + "/verification"

    @staticmethod
    def get_user_verification(code):
        code_as_string = str(code)
        verification = db_session.query(UserVerification.code == code_as_string).first()
        return verification

    @staticmethod
    def new_user(email):
        # XXX Check that the email isn't already used
        # XXX Actually, enforce that as a key restraint int the data model
        user = UserEntry(email)
        db_session.add(user)
        return user

    def new_user_with_password(self, email, password):
        user = self.new_user(email)
        user.set_password(password)
        user.force_verified()  # XXX Not very smart as a default

    # XXX This is a rather bogus method.
    def verify_user(self, code):
        vc = self.get_user_verification(code)
        if not vc:
            return False  # XXX Throw exception?
        elif not vc.verify(code):
            return False  # Throw exception?
        else:
            pass  # What?

    @staticmethod
    def find_all_users():
        users = db_session.query(UserEntry).all()
        if not users:
            users = []  # ?? XXX
        users_mapped = map(lambda u: u.as_map(), users)
        return users_mapped

    @staticmethod
    def find_user_by_api_key(api_key):
        api_key = str(api_key)
        user = db_session.query(UserEntry).filter(UserEntry.api_key == api_key).first()
        return user

    @staticmethod
    def find_user_by_id(user_id):
        user_id = str(user_id)
        user = db_session.query(UserEntry).filter(UserEntry.id == user_id).first()
        return user

    @staticmethod
    def find_user_by_email(email):
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
        return api_key, api_secret

    # ##############
    # XXX  Move to helper class Can we move the existance, deletion (basically
    # CRUD into a helper class, and thus compress the model classes somewhat?
    # XXX  This is dubious design!

    @staticmethod
    def check_and_return(user, checker, secret):
        if user and checker(secret):
            return user
        else:
            return None

    @staticmethod
    def delete_by_id(the_class, explanation, user_id):
        user_id = str(user_id)
        result = db_session.query(the_class).get(str(user_id))
        if result:
            db_session.delete(result)
        else:
            raise ModelException(explanation + " " + str(user_id), 404)
            # ##############

    def verify_api_login(self, api_key, api_secret):
        user = self.find_user_by_api_key(api_key)
        if not user:
            return None
        else:
            return self.check_and_return(user, user.check_api_key, api_secret)

    def verify_user_login(self, email_address, clair_text_password):
        user = self.find_user_by_email(email_address)
        if not user:
            return None
        else:
            return self.check_and_return(user, user.check_password, clair_text_password)

    @staticmethod
    def exists_user(user_id):
        user_id = str(user_id)
        result = db_session.query(exists().where(UserEntry.id == user_id)).scalar()
        return result

    def delete_user(self, user_id):
        self.delete_by_id(UserEntry, "Unknown User id", user_id)
