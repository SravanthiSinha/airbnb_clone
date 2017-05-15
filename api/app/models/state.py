from base import *


class State(BaseModel):
    name = CharField(max_length=128, null=False, unique=True)
