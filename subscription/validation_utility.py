import re
from appname.assets.blocked_emails import disposable_emails


def validate_email(email):
    if email is None:
        return "Email is required."
    elif not re.match(
        r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", email):
        return "Invalid Email Address."
    elif email.split('@')[-1] in disposable_emails:
        return "Disposable emails are not allowed."
    else:
        return None
