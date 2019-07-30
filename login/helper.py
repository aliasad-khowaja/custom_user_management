from passlib.hash import pbkdf2_sha256


class Helper:

    def get_hashed_password(password):
        return pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=20)