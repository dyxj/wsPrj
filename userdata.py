#!python3
"""
userdata.py
Stores user data
"""
import base_utils as bu


class BaseUser:
    """ Base class for users """

    def __init__(self, userid, password, email, name):
        self.userid = userid
        self.password = password
        self.email = email
        self.name = name

    def set_email(self, email):
        self.email = email

    def __str__(self):
        return "userid: {}\nemail: {}\nname: {}" \
            .format(self.userid, self.email, self.name)


def load_user_data(path):
    """
    :param path: location of json file
    :return: {str userid, BaseUser}
    """
    user_data = bu.load_json_from_file(path)
    user_dict = {}
    for u in user_data:
        user_dict[u.get("userid")] = BaseUser(u.get("userid"),
                                              u.get("password"),
                                              u.get("email"),
                                              u.get("name"))
    return user_dict
