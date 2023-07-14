import sys
from unittest import IsolatedAsyncioTestCase
import unittest
from unittest.mock import AsyncMock, Mock, patch, mock_open

# Test Utils
class UtilsTests(IsolatedAsyncioTestCase):

    # Test Author is pope
    def test_author_is_pope_true(self):
        sys.modules['constants'] = Mock()
        sys.modules['constants'].POPE_ROLE_ID = "9999"
        sys.modules['cardinal'] = __import__('src.cardinal')
        from src.utils import author_is_pope

        # Mock Pope role
        pope_role = Mock()
        pope_role.id = 9999
        pope_role.name = "Pope"
       
        #Mock a message with an Author
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        member.roles = [pope_role]

        message = AsyncMock()
        message.author = member

        mock_member_has_role = Mock()
        with patch('src.utils.member_has_role', mock_member_has_role):
            author_is_pope(message)
        assert mock_member_has_role.assert_called_once() == None


    def test_author_is_pope_false(self):
        sys.modules['constants'] = Mock()
        sys.modules['constants'].POPE_ROLE_ID = "1234567890"
        sys.modules['cardinal'] = __import__('src.cardinal')
        from src.utils import author_is_pope

        #Mock a message with an Author
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        member.roles = []

        message = AsyncMock()
        message.author = member

        mock_member_has_role = Mock()
        with patch('src.utils.member_has_role', mock_member_has_role):
            author_is_pope(message)
        assert mock_member_has_role.assert_called_once() == None


    def test_member_has_role_true(self):
        sys.modules['constants'] = Mock()
        sys.modules['cardinal'] = __import__('src.cardinal')
        from src.utils import member_has_role

        # Mock Pope role
        pope_role = Mock()
        pope_role.id = 9999
        pope_role.name = "Pope"
       
        #Mock a message with an Author
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        member.roles = [pope_role]

        message = AsyncMock()
        message.author = member

        assert member_has_role(member, 9999) == True


    def test_member_has_role_false(self):
        sys.modules['constants'] = Mock()
        sys.modules['cardinal'] = __import__('src.cardinal')
        from src.utils import member_has_role

        # Mock Pope role
        pope_role = Mock()
        pope_role.id = 9999
        pope_role.name = "Pope"
       
        #Mock a message with an Author
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        member.roles = [pope_role]

        message = AsyncMock()
        message.author = member

        assert member_has_role(member, 8888) == False


    def test_member_has_role_cant_access_roles(self):
        sys.modules['constants'] = Mock()
        sys.modules['cardinal'] = __import__('src.cardinal')
        from src.utils import member_has_role

        #Mock a message with an Author
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890

        message = AsyncMock()
        message.author = member

        with self.assertRaises(Exception):
            member_has_role(member, 8888)
        self.assertRaises(Exception)

    
    # # Test save cardinals json
    # def test_save_cardinals_json(self):
    #     from src.utils import save_cardinals_json
    #     from src.cardinal import Cardinal

    #     # Mock a member
    #     member = Mock()
    #     member.name = "Test Cardinal"
    #     member.id = 1234567890

    #     # Add mock to cardinal_list
    #     test_cardinal = Cardinal(member)
    #     test_cardinal_list = [test_cardinal] 

    #     # Mocks to capture function calls
    #     print_mock = Mock()
    #     json_mock = Mock()
    #     expected_json_output = [{'name': 'Test Cardinal', 'id': 1234567890, 'pope_points': 0, 'sin_coins': 0}]

    #     with patch('src.utils.cardinal_list', test_cardinal_list), patch('builtins.print', print_mock), patch('json.dump', json_mock):
    #         with patch('builtins.open', mock_open(read_data="data")) as mock_file:
    #             save_cardinals_json()
        
    #     # Check that the file was opened and written to with JSON
    #     mock_file.assert_called_once()
    #     json_mock.assert_called_once_with(expected_json_output, mock_file())
    #     assert print_mock.assert_called_once_with("Cardinals saved.") == None

    
    # # Test populate cardinals json
    # def test_populate_cardinals_json(self):
    #     sys.modules['cardinal'] = __import__('src.cardinal')
    #     from src.utils import populate_cardinals_json
    #     from src.cardinal import Cardinal

    #     # Mock a member
    #     member = Mock()
    #     member.name = "Test Cardinal"
    #     member.id = 1234567890

    #     # Mock guild
    #     mock_guild = Mock()
    #     mock_guild.get_member.return_value = member

    #     # Add mock to cardinal_list
    #     test_cardinal = Cardinal(member)
    #     test_cardinal_list = [test_cardinal] 

    #     # Mocks to capture function calls
    #     print_mock = Mock()
    #     test_file_data = '[{"name": "Test Cardinal", "id": 1234567890, "pope_points": 0, "sin_coins": 0}]'
    #     expected_json_output = MagicMock(return_value = json.loads('[{"name": "Test Cardinal", "id": 1234567890, "pope_points": 0, "sin_coins": 0}]'))

    #     with patch('src.utils.cardinal_list', test_cardinal_list), patch("builtins.print", print_mock),  patch('json.load', expected_json_output) as json_mock:
    #         with patch('builtins.open', new_callable=mock_open()) as mock_file:
    #             populate_cardinals_json(mock_guild)
        
    #     # Check that the file was opened and written to with JSON
    #     mock_file.assert_called_once()
    #     json_mock.assert_called_once()
    #     assert print_mock.assert_called_once_with("1 Cardinals populated from json.") == None

    
    # Test get_cardinal_by_id
    def test_get_cardinal_by_id(self):
        sys.modules['cardinal'] = __import__('src.cardinal')
        from src.utils import get_cardinal_by_id
        from src.cardinal import Cardinal

        # Mock a member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890

        # Add mock to cardinal_list
        test_cardinal = Cardinal(member)
        test_cardinal_list = [test_cardinal] 

        with patch('src.utils.cardinal_list', test_cardinal_list):
            assert get_cardinal_by_id(1234567890) == test_cardinal


    # Test get_member_from_cardinal_list
    def test_get_member_from_cardinal_list(self):
        sys.modules['cardinal'] = __import__('src.cardinal')
        from src.utils import get_member_from_cardinal_list
        from src.cardinal import Cardinal

        # Mock a member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890

        # Add mock to cardinal_list
        test_cardinal = Cardinal(member)
        test_cardinal_list = [test_cardinal] 

        with patch('src.utils.cardinal_list', test_cardinal_list):
            assert get_member_from_cardinal_list(member) == member

    # Test get_pope
    def test_get_pope(self):
        from src.cardinal import Cardinal
        from src.utils import get_pope
        
        # Mock Pope role
        pope_role = Mock()
        pope_role.id = 9999
        pope_role.name = "Pope"

        # Mock Cardinal role
        cardinal_role = Mock()
        cardinal_role.id = 8888
        cardinal_role.name = "Cardinal"
        
        # Mock a member
        member = Mock()
        member.name = "Test Pope"
        member.id = 1234567890
        member.roles = [pope_role]

        # Mock a member
        member2 = Mock()
        member2.name = "Test Cardinal"
        member2.id = 9876543210
        member2.roles = [cardinal_role]

        # Add mocks to cardinal_list
        test_cardinal = Cardinal(member)
        test_cardinal2 = Cardinal(member2)
        test_cardinal_list = [test_cardinal, test_cardinal2]

        mock_member_has_role = Mock()

        with patch("src.utils.cardinal_list", test_cardinal_list), patch("src.utils.member_has_role", mock_member_has_role):
            get_pope()
        self.assertEqual(mock_member_has_role.call_count, 1)

        # Invert list so pope is last and call again
        test_cardinal_list = [test_cardinal2, test_cardinal]
        with patch("src.utils.cardinal_list", test_cardinal_list), patch("src.utils.member_has_role", mock_member_has_role):
            get_pope()
        self.assertEqual(mock_member_has_role.call_count, 2)

        # Don't mock cardinal_list this time and verify returns None
        assert get_pope() == None


if __name__ == '__main__':
    unittest.main()