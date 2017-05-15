from base import *
from hashlib import *


class User(BaseModel):
    email = CharField(max_length=128, null=False, unique=True)
    password = CharField(max_length=128, null=False)
    first_name = CharField(max_length=128, null=False)
    last_name = CharField(max_length=128, null=False)
    is_Admin = BooleanField(default=False)

    def set_password(self, clear_password):
        ''' Sets the password in MD5 encryption '''
        passwd = md5()
        passwd.update(clear_password)
        self.password = passwd.hexdigest()
