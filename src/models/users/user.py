import uuid
import re

from src.common.database import Database
from src.common.utils import Utils
import src.models.users.erros as UserErrors
from src.models.alerts.alert import Alert
import src.models.users.constants as UserConstant


class User(object):
    def __init__(self,email, password, _id = None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id


    def __repr__(self):
        return "<User {}>".format(self.email)


    @staticmethod
    def is_login_valid(email, password):
        """
        :param email: the user's email
        :param password: the password(for security)
        :return:
        """
        #the password in the database is of pbkdf2_sha512
        #the password from user is sha512
        user_data = Database.find_one(collection=UserConstant.COLLECTION, query= {"email":email})
        if user_data is None:
            raise UserErrors.UserNotExistError("User not exist")
        if not Utils.check_hashed_password(password,user_data['password']):
            raise UserErrors.IncorrectPasswordError("Password not correct")
        return True

    @staticmethod
    def register_user(email, password):
        user_data = Database.find_one(collection=UserConstant.COLLECTION, query= {"email":email})
        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("User already registered")
        if not User.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The email format is invalid")
        User(email,Utils.hash_password(password)).save_to_db()
        return True

    @staticmethod
    def email_is_valid(email):
        email_matcher = re.compile('^[\w-]+@([\w-]+\.)+[\w-]+$')
        if email_matcher.match(email):
            return True
        else:
            return False


    def save_to_db(self):
        Database.insert(collection= 'users', data= self.json())

    def json(self):
        return {
            "_id":self._id,
            "email":self.email,
            "password":self.password
        }

    @classmethod
    def get_by_email(cls,user_email):
        return cls(**Database.find_one("users", {"email":user_email}))

    def get_alerts(self):
        return Alert.get_by_user_email(self.email)


