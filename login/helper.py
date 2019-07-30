from passlib.hash import pbkdf2_sha256


class Helper:

    @staticmethod
    def get_hashed_password(password):
        return pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=20)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        return pbkdf2_sha256.verify(password, hashed_password)