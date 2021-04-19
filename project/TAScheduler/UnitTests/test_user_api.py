from TAScheduler.ClassDesign.UserAPI import UserAPI, UserType
from django.test import TestCase


class TestUser(TestCase):

    def setUp(self):
        self.lname1 = 'smith'
        self.fname1 = 'bob'
        self.phone1 = '123-456-7890'
        self.univ_id1 = 'bsmith'
        self.password1 = 'password123'
        self.user_id1 = UserAPI.create_user(UserType.ADMIN, self.univ_id1, self.password1, self.lname1, self.fname1,
                                            self.phone1)

    def test_create_user(self):
        user_id = UserAPI.create_user(UserType.ADMIN, 'asmith','password456')
        self.assertTrue(user_id > 0, msg='Expecting id returned confirming saved to database.')

    #######################

    def test_get_user_by_user_id(self):
        user = UserAPI.get_user_by_user_id(self.user_id1)
        self.assertEqual(self.user_id1, user.user_id, msg='User id should be equal userId1')


    def test_get_user_by_univ_id(self):
        user = UserAPI.get_user_by_univ_id(self.univ_id1)
        self.assertEqual(self.univ_id1, user.univ_id, msg='Univ ID should be equal to user1s univ id.')


    def test_delete_user(self):
        user = UserAPI.get_user_by_user_id(self.user_id1)
        UserAPI.delete_user(user)
        user = UserAPI.get_user_by_user_id(self.user_id1)
        self.assertEqual(None, user, msg='Because we expect that the object is not in database.')

    def test_update_user(self):

        user = UserAPI.get_user_by_user_id(self.user_id1)
        print(user)
        lname2 = 'Foley'
        fname2 = 'B'
        phone2 = '456-123-7890'

        UserAPI.update_user(user, lname2, fname2, phone2)
        user = UserAPI.get_user_by_user_id(self.user_id1)
        print()
        self.assertEqual(lname2, user.l_name, msg='')
        self.assertEqual(fname2, user.f_name, msg='')
        self.assertEqual(phone2, user.phone,msg='')









