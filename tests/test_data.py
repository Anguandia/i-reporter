dat = {
    'basic': {'location': 'here', 'createdBy': 1, 'comment': 'flooding'},
    'optional': {'location': 'there', 'createdBy': 1, 'comment': 'flooding',
                 'type': 'intervention flag'},
    'resolved': {'location': 'where', 'createdBy': 1, 'comment': 'flooding',
                 'status': 'resolved'},
    'empty': {'location': '', 'createdBy': 1, 'comment': 'flooding', 'type':
              'intervention flag'},
    'invalid': {'location': 'here', 'createdBy': "1", 'comment': 'flooding'},
    'incomplete': {'location': 'here', 'createdBy': 1},
    'invalidComment': {'location': 'here', 'comment': '9', 'createdBy': 1}
}
