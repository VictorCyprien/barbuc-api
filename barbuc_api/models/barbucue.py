from typing import List

from mongoengine import Document, fields
from mongoengine.errors import ValidationError

import random

from .user import User

BARBUC_ID_MAX_VAL = 2**31-1

class Barbucue(Document):
    barbuc_id: int = fields.IntField(db_field="barbuc_id", min_value=0, max_value=BARBUC_ID_MAX_VAL, required=True, primary_key=True)
    """ ID of the barbucue
    """

    name: str = fields.StringField(required=True)
    """ Name of the barbucue
    """

    place: str = fields.StringField(required=True)
    """ Place of the barbucue
    """

    _date = fields.DateTimeField(db_field="date")
    """ Date of the barbucue
    """

    user = fields.ReferenceField(User)
    """ User who reserved the barbucue
    """


    @property
    def date(self):
        return self._date


    @date.setter
    def date(self, time):
        self._date = time
    

    @classmethod
    def create(cls, input_data: dict):
        barbucue = Barbucue()
        if 'barbuc_id' not in input_data:
            input_data['barbuc_id'] = cls._next_id()
        if 'name' in input_data:
            name = input_data['name']
            del input_data['name']
        if 'place' in input_data:
            place = input_data['place']
            del input_data['place']
        if 'date' in input_data:
            date = input_data['date']
            del input_data['date']

        barbucue.barbuc_id = input_data['barbuc_id']
        barbucue.name = name
        barbucue.place = place

        # Set date of barbucue
        barbucue.date = date
        return barbucue
    

    def update(self, input_data: dict):
        if "name" in input_data:
            new_name = input_data["name"]
            self.name = new_name
        if "place" in input_data:
            new_place = input_data["place"]
            self.place = new_place
        if "date" in input_data:
            new_date = input_data["date"]
            self.date = new_date


    @classmethod
    def _next_id(cls) -> int:
        uid = random.randint(0, BARBUC_ID_MAX_VAL)
        nb_trial = 0
        while cls.objects(pk=uid).count() and nb_trial < 10:
            uid = random.randint(0, BARBUC_ID_MAX_VAL)
            nb_trial += 1
        if nb_trial > 10:
            raise RuntimeError("Impossible to get new barbucue id")
        return uid


    @classmethod
    def get_by_id(cls, id: int, only: List[str] = None, exclude: List[str] = None) -> "Barbucue":
        try:
            id = int(id)
        except ValueError:
            raise ValidationError('barbuc_id should be an int')
        _query = Barbucue.objects(barbuc_id=id)
        if only is not None:
            _query = _query.only(*only)
        if exclude is not None:
            _query = _query.exclude(*exclude)
        barbucue = _query.get()
        return barbucue
