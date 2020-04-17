"""User Request"""

#Django
from django.test import TestCase
from django.contrib.auth.hashers import make_password

# Django REST Framework
from rest_framework.test import APITestCase
from rest_framework import status

# Models
from myhandycrafts.users.models import User,Profile
from myhandycrafts.categories.models import Category

# Utils
import json
from myhandycrafts.utils.token import get_response_token



class UserAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            first_name='fer',
            last_name='Alvarez',
            email='falvarez@gmail.com',
            username='feralvarez',
            password='admin123',
        )

        self.user = User.objects.create(
            first_name='fer',
            last_name='Alvarez',
            email='fer.alvarez@mail.com',
            username='fer.alvarez',
            password=make_password('admin123'),
            type_user='B',
            is_verified=True,
            is_active=True,
            is_craftsman=True,
            created_by=1,
            is_staff=True
        )

        self.category = Category.objects.create(
            name='lana',
            description='Artesanias de lana de oveja, alpaca, llama,y otros camelidos'
        )


        self.profile = Profile.objects.create(
            user=self.user,
            biography = 'biagraphy',
            ci = '123456lp',
            birth_date = '2020-01-01',
            address = 'calle perdida',
            category=self.category,
            # Company information
            nit = '',
            nit_bussiness_name = '',
            nit_is_active = False,

            # Contact Information User
            phone_number = '76543211',
            website = 'www.cosas.com.bo',
            has_wattsapp = False,
            has_facebook = False,
            addres_facebook = 'www.f.com/miusuario'
        )
        # self.access_token =
        # token = 'token'
        # self.client.credentials(HTTP_AUTHORIZATION='bearer {}',token)


        self.access_token = get_response_token(self.user.pk, False)['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.access_token))



    def  test_user_login(self):
        url = '/users/login/'
        data = {
            "email": "fer.alvarez@mail.com",
            "password": "admin123"
        }
        """success when de code is 200"""
        response = self.client.post(url,data=data,format='json')

        # import pdb;
        # pdb.set_trace()
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = json.loads(json.dumps(response.data))
        self.assertTrue('state' in data)
        self.assertEqual(data['state'],1)
        self.assertTrue('data' in data)
        self.assertTrue('message' in data)
        self.assertTrue('user' in data['data'])
        self.assertTrue('token' in data['data'])

        self.assertTrue('access_token' in data['data']['token'])
        self.assertTrue('refresh_token' in data['data']['token'])

        # self.access_token = data['data']['token']['access_token']



    def test_update_password(self):

        url = '/users/updatepassword/'
        data = {
            'password':'admin123'
        }


        response = self.client.post(url,
                                    data=data,
                                    format='json')
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.access_token))

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = json.loads(json.dumps(response.data))
        self.assertTrue('state' in data)
        self.assertEqual(data['state'],1)


    def test_email_send_recover(self):
        url = '/users/recovery/'
        data={
            'email':'fer.alvarez@mail.com'
        }
        response = self.client.post(url,data=data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = json.loads(json.dumps(response.data))
        self.assertTrue('state' in data)
        self.assertEqual(data['state'], 1)

    def test_signup(self):
        url='/users/register/'
        data={
            "email": "violet@mail.com",
            "username": "violet",
            "password": "1234567",
            "first_name": "violet",
            "last_name": "Gonzales",
            "biography": "Ciudadana boliviana de La Paz city",
            "ci": "76543 OR",
            "birth_date": "2018-02-02",
            "address": "Calle perdida",
            "category": self.category.pk,
            "nit": "123",
            "nit_bussiness_name": "vende cositas",
            "nit_is_active": True,
            "phone_number": "+198 27049821",
            "website": "www.perrunos.com",
            "has_wattsapp": True,
            "has_facebook": True,
            "addres_facebook": "www.face.com/busquedayrescate"
        }

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(json.dumps(response.data))
        self.assertTrue('state' in data)
        self.assertEqual(data['state'], 1)










