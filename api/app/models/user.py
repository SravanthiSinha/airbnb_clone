from base import *
from hashlib import md5


class User(BaseModel):
    email = CharField(max_length=128, null=False, unique=True)
    password = CharField(max_length=128, null=False)
    first_name = CharField(max_length=128, null=False)
    last_name = CharField(max_length=128, null=False)
    is_Admin = BooleanField(default=False)

    def set_password(self, clear_password):
        ''' Sets the password in MD5 encryption '''
        self.password = md5(clear_password).hexdigest()

    def to_hash(self):
        ''' Returns a hash of the User in the database '''
        data = {}
        data['email'] = self.email
        data['first_name'] = self.first_name
        data['last_name'] = self.last_name
        data['is_admin'] = self.is_Admin
        return super(User, self).to_hash(self, data)
