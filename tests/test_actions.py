import unittest, os, sys
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock, patch
from src.cardinal import Cardinal


class ActionsTests(IsolatedAsyncioTestCase):

    def setUp(self):
        #Suppress print statements
        import sys
        sys.stdout = open(os.devnull, 'w')
        
        #Suppress warnings
        import warnings
        warnings.filterwarnings("ignore")


    # Test Actions absolve
    @patch('os.getenv')
    async def test_actions_absolve(self, mock_getenv):
        # Point our secondary imports to correct locations
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        
        from src.actions import absolve
       
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        
        test_cardinal = Cardinal(member)
        test_cardinal.add_sin_coins(10)
        test_cardinal_list = [test_cardinal]
        assert test_cardinal_list[0].sin_coins == 10

        with patch('src.actions.cardinal_list', test_cardinal_list):
            channel = AsyncMock()
            channel.send = AsyncMock()
            await absolve(member, channel)
            assert test_cardinal.sin_coins == 0
            assert channel.send.assert_called_once_with(f"<@{member.id}>, You have been absolved of all your sins!") == None


if __name__ == '__main__':
    unittest.main()