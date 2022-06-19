from dataclasses import dataclass
from datetime import date


@dataclass
class AddUserRequestData:
    user_name: str
    email_id: str
    gender: str
    dob: date
    password: str
