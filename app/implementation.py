from .models import RedFlag
import datetime

red_flags = {}


class Implementation:
    def create(self, data):
        others = {
            'type': 'red-flag', 'status': 'draft', 'videos': '', 'images': '',
            'comment': ''}
        red_flag = RedFlag(
            (len(red_flags)+1), data['location'], data['createdBy'],
            data['title']
            )
        red_flag.__setattr__('createdOn', datetime.datetime.now())
        for key in others:
            if key in data:
                red_flag.__setattr__(key, data[key])
            else:
                red_flag.__setattr__(key, others[key])
        red_flags[str(red_flag.id)] = red_flag.__dict__
        return [
            201, 'data', [{'id': red_flag.id, 'message': 'Created red flag'}]
            ]

    def get_flags(self):
        res = [200, 'data', [red_flags[key] for key in red_flags.keys()]]
        return res

    def get_flag(self, red_flag_id):
        try:
            red_flag = red_flags[str(red_flag_id)]
            res = [200, 'data', [red_flag]]
        except Exception as e:
            print(e)
            res = [200, 'data', []]
        return res

    def edit(self, red_flag_id, data, field):
        red_flag = self.get_flag(red_flag_id)[2]
        if len(red_flag) == 0:
            res = [400, 'error', 'red flag not found']
        elif red_flag[0]['status'] in ['rejected', 'resolved']:
            res = [
                403, 'error', f'red flag already {red_flag[0]["status"]}'
                ]
        elif field == 'location' and 'geolocation' not in red_flag[0][
                'location']:
            red_flag[0]['location'] += ' ' + data['location']
            res = 'added'
        elif field == 'location' and 'geolocation' in red_flag[0]['location']:
            red_flag[0]['location'] =\
                    red_flag[0]['location'][:red_flag[0]['location'].index(
                        'geolocation')] + data['location']
            res = 'updated'
        else:
            red_flag[0][field] = data[field]
            res = 'updated'
        if isinstance(res, str):
            result = [200, 'data', [{
                'id': int(red_flag_id), 'message':
                f'{res} red-flag record\'s {field}'}]]
        else:
            result = res
        return result

    def delete(self, red_flag_id):
        try:
            red_flags.pop(str(red_flag_id))
            res = [200, 'data', [{'id': int(red_flag_id), 'message':
                                 'red-flag record has been deleted'}]]
        except Exception:
            res = [404, 'error', 'red flag not found']
        return res
