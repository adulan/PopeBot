import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, Mock, mock_open, patch


class TestUtilsNonAsync(unittest.TestCase):

    # Some of the utils tests don't work with the IsolatedAsyncioTestCase, so run them from here
    # RuntimeWarning: Enable tracemalloc to get the object allocation traceback

    # Test populate cardinals json
    def test_populate_cardinals_json(self):
        sys.modules['constants'] = Mock()
        sys.modules['cardinal'] = Mock()
        from src.utils import populate_cardinals_json
        from src.cardinal import Cardinal

        # Mock a member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890

        # Add mock to cardinal_list
        test_cardinal = Cardinal(member)
        test_cardinal_list = [test_cardinal] 

        # Mocks to capture function calls
        print_mock = Mock()
        json_mock = MagicMock(return_value=[{'name': 'Test Cardinal', 'id': 1234567890, 'pope_points': 0, 'sin_coins': 0}])
        #expected_json_output = 
        #json_mock.return_value = expected_json_output
        mock_guild = Mock()

        cardinal_mock = Mock(return_value=test_cardinal)
        
        from_json_mock = MagicMock(return_value=True)
        from_json_mock.from_json.return_value = test_cardinal
        cardinal_mock.from_json = Mock()

        with patch('src.utils.cardinal_list', test_cardinal_list),  patch('json.load', json_mock):
            with patch('builtins.open', mock_open(read_data="data")) as mock_file, patch('builtins.print', print_mock):
                populate_cardinals_json(mock_guild)
        
        # Check that the file was opened and written to with JSON
        mock_file.assert_called_once()
        json_mock.assert_called_once_with(mock_file())
        assert print_mock.assert_called_once_with("1 Cardinals populated from json.") == None

    
    # Test populate cardinals
    async def test_populate_cardinals(self):
        sys.modules['constants'] = Mock()
        sys.modules['cardinal'] = Mock()
        from src.utils import populate_cardinals
        from src.cardinal import Cardinal

        # Mock Cardinal role
        cardinal_role = Mock()
        cardinal_role.id = 1111
        cardinal_role.name = "Cardinal"

        # Mock a member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        member.roles = [cardinal_role]

        # Add mock to cardinal_list
        test_cardinal = Cardinal(member)
        test_cardinal_list = [test_cardinal] 

        # Mocks to capture function calls
        print_mock = Mock()
        json_mock = MagicMock(return_value=[{'name': 'Test Cardinal', 'id': 1234567890, 'pope_points': 0, 'sin_coins': 0}])

        mock_client = AsyncMock()
        mock_guild = MagicMock()
        mock_guild.members = [member]
        mock_client.get_guild.return_value = mock_guild

        cardinal_mock = Mock(return_value=test_cardinal)
        
        from_json_mock = MagicMock(return_value=True)
        from_json_mock.from_json.return_value = test_cardinal
        cardinal_mock.from_json = Mock()

        with patch('src.utils.cardinal_list', test_cardinal_list),  patch('json.load', json_mock):
            with  patch('builtins.print', print_mock):
                await populate_cardinals(mock_client)
        
        # Check that two messages were printed
        # print("No cardinal_list.json found. Populating from guild.")
        # print("Cardinals populated.")
        self.assertEqual(print_mock.call_count, 2)

if __name__ == '__main__':
    unittest.main()