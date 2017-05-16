from base import *
from state import State


class City(BaseModel):
    name = CharField(max_length=128, null=False)
    state = ForeignKeyField(
        rel_model=State,
        related_name="cities",
        on_delete="CASCADE")

    def to_hash(self):
        state = State.get(State.id == self.state)
        data = {}
        data['name'] = self.name
        data['state_id'] = state.id
        return super(City, self).to_hash(self, data)
