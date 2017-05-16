"""
Unittest cases for the API routes to /states/*
"""
from base import BaseTestCase
from app.models.state import State
import json
from data import states


class StateTestCase(BaseTestCase):
    table = [State]
    path = '/states'

    example = states[0]

    def test_create(self):
        # It should create states with sequential ids.
        count = 1
        for state in states:
            last_state = self.create_row(state, '201 CREATED')
            self.check(last_state.id, count)
            self.check(last_state.name, state['name'])
            count += 1
        # It should return code 10001 when trying to create duplicated
        # state name.
        dupl_state = {'name': 'California'}
        last_state = self.check_dupl_entry(dupl_state, 10001)
        # The last entry on database should be the previous one
        self.check(last_state.name, 'Alaska')

    def test_list(self):
        self.check_list()

    def test_get(self):
        self.check_get('State')

    def test_delete(self):
        self.check_delete('State')
