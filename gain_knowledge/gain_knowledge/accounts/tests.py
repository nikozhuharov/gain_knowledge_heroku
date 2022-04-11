import logging
from datetime import date

from django import test as django_test
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse

from gain_knowledge.accounts.models import Profile

UserModel = get_user_model()


class ProfileTests(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': '12345qew',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'User',
        'picture': 'images/profile/Football_soccer_ball.svg_MGbi4yq.png',
        'date_of_birth': date(1990, 4, 13),
        'email': 'test@test.com',
        'gender': 'Male'
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        return (user, profile)

    def __get_response_for_profile(self, profile):
        return self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))


    def test_when_user_is_owner__expect_is_owner_to_be_true(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.__get_response_for_profile(profile)

        self.assertTrue(response.context['is_owner'])

    def test_when_user_is_not_owner__expect_is_owner_to_be_false(self):
        _, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'testuser2',
            'password': '12345qwe',
        }

        self.__create_user(**credentials)

        self.client.login(**credentials)

        response = self.__get_response_for_profile(profile)

        self.assertFalse(response.context['is_owner'])

    def test_profile_create__when_first_name_contains_only_letters__expect_success(self):
        _, profile = self.__create_valid_user_and_profile()
        profile.save()
        self.assertIsNotNone(profile.pk)

    def test_profile_create__when_first_name_contains_a_digit__expect_to_fail(self):
        first_name = 'Bobi1'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            picture=self.VALID_PROFILE_DATA['picture'],
            date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
            email=self.VALID_PROFILE_DATA['email'],
            gender=self.VALID_PROFILE_DATA['gender'],
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_dollar_sign__expect_to_fail(self):
        first_name = 'Bobi$'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            picture=self.VALID_PROFILE_DATA['picture'],
            date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
            email=self.VALID_PROFILE_DATA['email'],
            gender=self.VALID_PROFILE_DATA['gender'],
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_space__expect_to_fail(self):
        first_name = 'Bo bi'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            picture=self.VALID_PROFILE_DATA['picture'],
            date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
            email=self.VALID_PROFILE_DATA['email'],
            gender=self.VALID_PROFILE_DATA['gender'],
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)