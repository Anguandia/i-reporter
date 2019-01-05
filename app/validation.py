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

    def validateRoute(self, resource):
        if resource != 'red_flags':
            res = [400, 'error', f'wrong url, check \'{resource}\'']
            return res

    def validateDuplicate(self, data):
        flags = Implementation().get_flags()[2]
        for flag in flags:
            if data['location'] in flag['location'] and data['title']\
                    == flag['title']:
                return [
                    200, 'data', [
                        {'id': flag['id'], 'message': 'red flag exists'}
                        ]
                    ]

    def validateBasics(self, data):
        for field in ['location', 'comment', 'createdBy', 'title']:
            if field not in data:
                return [
                    400, 'error',
                    f'{field} field missing, invalid key or incorrect'
                    ]
            elif not data[field]:
                return [400, 'error', 'please submit {}'.format(field)]

    def validateDescriptive(self, data):
        for field in ['location', 'comment', 'title']:
            if field and not self.validateInt(
                    data[field]):
                return [
                    400, 'error', f'{field} must be descriptive'
                    ]

    def validateNew(self, data):
        if self.validateBasics(data):
            result = self.validateBasics(data)
        elif self.validateDescriptive(data):
            result = self.validateDescriptive(data)
        elif self.bad_type(data):
            result = self.bad_type(data)
        elif self.validateDuplicate(data):
            result = self.validateDuplicate(data)
        else:
            result = Implementation().create(data)
        return result

    def validateEdit(self, data, red_flag_id, field):
        if field not in ['location', 'comment', 'status']:
            result = [400, 'error', f'wrong endpoint \'{field}\'']
        # check error in data key vs endpoint specification
        elif field not in data:
            result = [
              400, 'error',
              f'{field} key missing, check your input or url'
              ]
        # safeguard against accidental deleting of field data
        elif not data[field]:
            result = [400, 'error', f'submit new {field}']
        elif field == 'location' and ' ' in data['location']:
            d = data['location'].split(' ')
            result = Implementation().edit(red_flag_id, {
                'location': 'geolocation ' + f'N: {d[0]}, E: {d[1]}'},
                'location')
        elif field == 'location' and ' ' not in data['location']:
            result = [
                400, 'error',
                "location must be of format'latitude <space> longitude'"
                ]
        else:
            result = Implementation().edit(red_flag_id, data, field)
        return result

    '''validation for id in url'''
    @staticmethod
    def validateInt(data):
        try:
            int(data)
        except Exception:
            return 'id must be a number'
