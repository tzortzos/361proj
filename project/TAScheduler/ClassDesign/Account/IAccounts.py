from abc import ABC, abstractmethod

class AccountInterface(ABC):

    @abstractmethod
    def get_User_id(self):
        pass

    def get_type(self):
        pass

    def get_univ_id(self):
        pass

    def get_lname(self):
        pass

    def set_lname(self, lname):
        pass

    def get_fname(self):
        pass

    def set_fname(self, fname):
        pass

    def get_phone(self):
        pass

    def set_phone(self, phone):
        pass

    def get_password(self):
        pass

    def set_password(self, password):
        pass