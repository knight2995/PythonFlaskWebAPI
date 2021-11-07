

class UserDuplicatedException(Exception):
    def __init__(self):
        super().__init__('이미 존재하는 id 입니다.')

    def __str__(self):
        return '이미 존재하는 id 입니다.'

class AlbumDuplicatedException(Exception):
    def __init__(self):
        super().__init__('이미 존재하는 id 입니다.')

    def __str__(self):
        return '이미 존재하는 id 입니다.'
