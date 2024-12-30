import re

def is_valid_login(login):
   if not login:
        return False
   pattern = r"^[a-zA-Z0-9_]{3,20}$"
   if re.match(pattern, login):
        return True
   return False

def is_valid_password(password):
    if not password:
        return False
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]).{8,30}$"
    if re.match(pattern,password):
        return True
    return False

def is_valid_jwt(jwt_token):
    if not jwt_token:
        return False
    pattern = r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$"
    if re.match(pattern,jwt_token):
        return True
    return False