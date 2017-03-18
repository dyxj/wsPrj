#! python3
"""
msgbuilder.py
Build messages
"""


class BaseMsg:
    def __init__(self, msg_list=None):
        if msg_list is None:
            self.msg_list = []
        else:
            self.msg_list = msg_list

    def add_message(self, msg):
        if msg not in self.msg_list:
            self.msg_list.append(msg)

    def remove_message(self, msg):
        if msg in self.msg_list:
            self.msg_list.remove(msg)

    def index_msg_list(self):
        indexmsg = ""
        for i, msg in enumerate(self.msg_list):
            indexmsg += 'msg[{}] : {}\n'.format(i, msg)

    def build_str(self):
        fullmsg = ""
        for msg in self.msg_list:
            fullmsg += msg + "\n"
        return fullmsg

    def __str__(self):
        return self.build_str()


class EmailObj(BaseMsg):
    def __init__(self, user, email_add, msg_list=None):
        super().__init__(msg_list)
        self.user = user
        self.email_add = email_add

    def __str__(self):
        msgstr = 'user : {}\n'.format(self.user)
        msgstr += 'email address : {}\n'.format(self.email_add)
        msgstr += self.build_str()
        return msgstr
