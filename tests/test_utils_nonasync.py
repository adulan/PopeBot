import sys, os
import unittest
from unittest.mock import AsyncMock, MagicMock, Mock, mock_open, patch


class TestUtilsNonAsync(unittest.TestCase):

    # Some of the utils tests don't work with the IsolatedAsyncioTestCase, so run them from here
    # RuntimeWarning: Enable tracemalloc to get the object allocation traceback
    
    def setUp(self):
        #Suppress print statements
        import sys
        sys.stdout = open(os.devnull, 'w')
        
        #Suppress warnings
        import warnings
        warnings.filterwarnings("ignore")
   
   
    # Test populate cardinals json
    # def test_populate_cardinals_json(self):
    #     sys.modules['constants'] = Mock()
    #     sys.modules['cardinal'] = Mock()
    #     from src.utils import populate_cardinals_json
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
    #     json_mock = MagicMock(return_value=[{'name': 'Test Cardinal', 'id': 1234567890, 'pope_points': 0, 'sin_coins': 0}])

    #     mock_guild = Mock()

    #     cardinal_mock = Mock(return_value=test_cardinal)
        
    #     from_json_mock = MagicMock(return_value=True)
    #     from_json_mock.from_json.return_value = test_cardinal
    #     cardinal_mock.from_json = Mock()

    #     with patch('src.utils.cardinal_list', test_cardinal_list),  patch('json.load', json_mock):
    #         with patch('builtins.open', mock_open(read_data="data")) as mock_file, patch('builtins.print', print_mock):
    #             populate_cardinals_json(mock_guild)
        
    #     # Check that the file was opened and written to with JSON
    #     mock_file.assert_called_once()
    #     json_mock.assert_called_once_with(mock_file())
    #     assert print_mock.assert_called_once_with("1 Cardinals populated from json.") == None

    


if __name__ == '__main__':
    unittest.main()