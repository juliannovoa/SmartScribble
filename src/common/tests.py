#  Copyright 2020 Julián Novoa Martín
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

#  Copyright 2020 Julián Novoa Martín
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

#  Copyright 2020 Julián Novoa Martín
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from common.util_test import get_logged_users


class UtilTestTest(TestCase):

    @staticmethod
    def get_test_username(user_number: int) -> str:
        return f'test_user{user_number}'

    @staticmethod
    def get_test_password(user_number: int) -> str:
        return f'qawsedrftgyh{user_number}'

    @staticmethod
    def create_test_users(number_of_users: int) -> None:
        for i in range(number_of_users):
            user = User.objects.create(username=UtilTestTest.get_test_username(i))
            user.set_password(UtilTestTest.get_test_password(i))
            user.save()

    def test_get_logged_users(self) -> None:
        UtilTestTest.create_test_users(2)
        users_set = set(User.objects.all())
        for i in range(len(users_set)):
            c = Client()
            c.login(username=UtilTestTest.get_test_username(i), password=UtilTestTest.get_test_password(i))
        logged_users_set = set(get_logged_users())
        self.assertEqual(logged_users_set, users_set)
