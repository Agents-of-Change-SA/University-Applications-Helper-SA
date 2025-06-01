# from rest_framework.test import APITestCase
# from django.urls import reverse
# from rest_framework import status

# # Create your tests here.
# class AccountsTestCase(APITestCase):
#     def setUp(self):
#         self.register_url = reverse('accounts:register')
#         self.login_url = reverse('accounts:login')
#         self.logout_url = reverse('accounts:logout')
#         self.profile_url = reverse('accounts:profile')

#         self.user_data = {
#             'email': 'testuser@example.com',
#             'password': 'StrongPass123!',
#             'first_name': 'Test',
#             'last_name': 'User',
#             'id_number': '9901015800081',  # Example valid SA ID
#             'phone_number': '0812345678',
#             'is_citizen': True
#         }


#         # Register the user
#         self.client.post(self.register_url, self.user_data, format='json')

#     def test_register_user_valid(self):
#         data = {
#             "username": "newuser",
#             "email": "newuser@example.com",
#             "password": "NewValid123!"
#         }
#         response = self.client.post(self.register_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_register_user_weak_password(self):
#         data = {
#             "username": "weakuser",
#             "email": "weak@example.com",
#             "password": "weak"  # too weak
#         }
#         response = self.client.post(self.register_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('password', response.data)

#     def test_login_user_success(self):
#         response = self.client.post(self.login_url, {
#             "username": self.user_data["username"],
#             "password": self.valid_password
#         }, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('access', response.data)

#     def test_login_user_fail(self):
#         response = self.client.post(self.login_url, {
#             "username": self.user_data["username"],
#             "password": "WrongPassword!"
#         }, format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_logout_user(self):
#         login_response = self.client.post(self.login_url, {
#             "username": self.user_data["username"],
#             "password": self.valid_password
#         }, format='json')

#         access_token = login_response.data['access']
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

#         logout_response = self.client.post(self.logout_url, {}, format='json')
#         self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)

#     def test_profile_view_authenticated(self):
#         login_response = self.client.post(self.login_url, {
#             "username": self.user_data["username"],
#             "password": self.valid_password
#         }, format='json')

#         token = login_response.data['access']
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

#         response = self.client.get(self.profile_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['email'], self.user_data['email'])

#     def test_profile_view_unauthenticated(self):
#         response = self.client.get(self.profile_url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

