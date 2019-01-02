import datetime


class RedFlag:
    def __init__(
        self, id, location, createdBy, comment,
            createdOn=datetime.datetime.utcnow(), type='red-flag',
            status='Draft',   images=False, videos=False
            ):
        self.id = id
        self.location = location
        self.createdBy = createdBy
        self.comment = comment
        self.createdOn = createdOn
        self.type = type
        self.status = status
        self.images = images
        self.videos = videos

    def __repr__(self):
        return (f'location: {self.location}, createdOn: {self.createdOn}')
