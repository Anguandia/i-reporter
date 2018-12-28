from .models import RedFlag
import datetime

red_flags = {}


class Implementation:
    def create(self, data):
        red_flag = RedFlag(
            (len(red_flags)+1), data['location'], data['createdBy'],
            data['comment']
            )
        for field in data:
            if field not in ['location', 'createdBy', 'comment']:
                red_flag.__setattr__(field, data[field])
        red_flags[str(red_flag.id)] = red_flag.__dict__
        return [
            201, 'data', [{'id': red_flag.id, 'message': 'Created red flag'}]
            ]
