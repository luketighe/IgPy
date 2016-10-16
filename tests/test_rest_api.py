import unittest
from unittest.mock import patch

from igpy.rest_api import IGRestApi


def mocked_requests_post_error(status, **kwargs):

    class ErrorResponse:
        def __init__(self):
            self.status_code = '400'

    return ErrorResponse()


class IGRestApiTest(unittest.TestCase):

    @patch('requests.post')
    def test_should_not_login(self, requests_mock):

        # arrange
        requests_mock.side_effect = mocked_requests_post_error
        ig_rest = IGRestApi('username', 'password', 'api_key', 'url')

        # act
        with self.assertRaises(PermissionError) as context:
            ig_rest.login()

        # assert
        self.assertTrue('Could not log in. Http code: 400' in str(context.exception))


    def test_should_login_and_return_true(selfself, requests_mock):
        # arrange
        requests_mock.side_effect
