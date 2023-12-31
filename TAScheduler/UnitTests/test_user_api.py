from TAScheduler.ClassDesign.UserAPI import UserAPI, UserType
from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from django.test import TestCase
import more_itertools
from TAScheduler.models import User


class TestUser(TestCase):

    def setUp(self):
        self.lname1 = 'smith'
        self.fname1 = 'bob'
        self.phone1 = '123-456-7890'
        self.username1 = 'bsmith'
        self.password1 = 'password123'
        self.id1 = User.objects.create(
            type=UserType.ADMIN,
            username=self.username1,
            password=self.password1,
            l_name=self.lname1,
            f_name= self.fname1,
            phone=self.phone1)
        self.id2 = User.objects.create(type=UserType.PROF,username='ateacher',password='Password456')

    def test_create_user(self):
        user_id = UserAPI.create_user(UserType.ADMIN, 'asmith','password456')
        self.assertTrue(user_id > 0, msg='Expecting id returned confirming saved to database.')

    def test_get_user_by_user_id(self):
        user = UserAPI.get_user_by_user_id(self.id1.id)
        self.assertEqual(self.id1.id, user.id, msg='User id should be equal userId1')

    def test_get_user_by_username(self):
        user = UserAPI.get_user_by_univ_id(self.username1)
        self.assertEqual(self.username1, user.username, msg='Univ ID should be equal to user1s univ id.')

    def test_get_all_users(self):
        user_set = UserAPI.get_all_users()
        list_of_users = list(user_set)
        length = more_itertools.ilen(list_of_users)
        self.assertEqual(2, length, msg='Expected list of courses to be 2.')
        self.assertTrue(self.id1 in list_of_users, msg='Exepect course1 in all courses.')
        self.assertTrue(self.id1 in list_of_users, msg='Expected course2 in all courses.')

    def test_delete_user(self):
        response = UserAPI.delete_user(self.id1.id)
        self.assertEqual(True, response, msg='Because we expect that the object is not in database.')

    def test_update_user(self):
        user = UserAPI.get_user_by_user_id(self.id2.id)
        lname2 = 'Foley'
        fname2 = 'B'
        phone2 = '456-123-7890'
        UserAPI.update_user(user, lname2, fname2, phone2)
        user = UserAPI.get_user_by_user_id(self.id2.id)
        self.assertEqual(lname2, user.l_name, msg='')
        self.assertEqual(fname2, user.f_name, msg='')
        self.assertEqual(phone2, user.phone,msg='')

    def test_update_password(self):
        new_password = 'NewPassword123'
        user = UserAPI.get_user_by_user_id(self.id1.id)
        LoginUtility.update_password(user, new_password)
        user = UserAPI.get_user_by_user_id(self.id1.id)
        self.assertEqual(new_password, user.password, msg="Password is expected to be updated with new password.")
        self.assertEqual(False, user.password_tmp, msg='Failed because expected tmp password was updated.')

    def test_check_user_type(self):
        user = UserAPI.get_user_by_user_id(self.id1.id)
        self.assertEqual('A', user.type, msg="Expected Admin as type for user1")

    def test_empty_user_type(self):
        with self.assertRaises(TypeError):
            new_user = UserAPI.create_user('', 'asmith', 'password456')

    def test_empty_username(self):
        new_user = UserAPI.create_user(UserType.ADMIN, self.username1, self.password1)
        user = UserAPI.get_user_by_user_id(new_user)
        self.assertTrue(user.username, msg='University ID can not be empty')

    def test_empty_password(self):
        with self.assertRaises(TypeError):
            new_user = UserAPI.create_user(UserType.ADMIN, self.id1, '')
