class UserDuplicatedException(Exception):
    def __init__(self):
        super().__init__('이미 존재하는 id 입니다.')

    def __str__(self):
        return '이미 존재하는 id 입니다.'


class AlbumDuplicatedException(Exception):
    def __init__(self):
        super().__init__('이미 존재하는 이름 입니다.')

    def __str__(self):
        return '이미 존재하는 이름 입니다.'


class ForbiddenException(Exception):
    def __init__(self):
        super().__init__('잘못된 접근입니다.')

    def __str__(self):
        return '잘못된 접근입니다.'


class NotExistUser(Exception):
    def __init__(self):
        super().__init__('존재하지 않는 회원입니다.')

    def __str__(self):
        return '존재하지 않는 회원입니다.'