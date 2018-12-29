from .models import RedFlag
import datetime
from app.implementation import Implementation


class Validation:
    data_types = {
        'id': int,
        'createdOn': datetime.datetime,
        'createdBy': int,
        'type': str,
        'location': str,
        'status': str,
        'Images': str,
        'Videos': str,
        'comment': str
        }

    def bad_type(self, data):
        for field in data:
            if field in self.data_types and not isinstance(
                    data[field], self.data_types[field]):
                return [
                    400, 'error',
                    f'{field} should be of type {self.data_types[field]}'
                    ]
            # check forinvalid keys in data
            elif field not in self.data_types:
                return [400, 'error', f'unknown input {field}']

    def validateNew(self, data):
        if self.bad_type(data):
            return self.bad_type(data)
        else:
            for field in ['location', 'comment', 'createdBy']:
                if field not in data:
                    return [
                      400, 'error',
                      f'{field} field missing, invalid key or incorrect'
                      ]
                if not data[field]:
                    return [400, 'error', 'please submit {}'.format(field)]
            result = Implementation().create(data)
            return result

    def validateEdit(self, data, red_flag_id, field):
        # Check if end point is valid
        if field not in self.data_types:
            result = [
              400, 'error', f'no field {field} in red flag, check your request'
              ]
        # check if editing is authorizes for field
        elif field not in ['location', 'comment']:
            result = [403, 'error', f'{field} can not be changed']
        # check error in data jey vs endpoint specification
        elif field not in data:
            result = [
              403, 'error',
              f'{field} key missing, check your input or url'
              ]
        # safeguard against accidental deleting of field data
        elif not data[field]:
            result = [400, 'error', f'submit new {field}']
        else:
            result = Implementation().edit(red_flag_id, data, field)
        return result
