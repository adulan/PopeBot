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
        # Account for directory differences between test and src
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, check_for_pope_change
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].armageddon = False
        from src.actions import absolve
       
        # Setup mock Discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        
        # Create a cardinal using the mock member
        test_cardinal = Cardinal(member)
        test_cardinal.sin_coins = 10
        test_cardinal_list = [test_cardinal]
        # Check that mock's sin coins were applied
        assert test_cardinal_list[0].sin_coins == 10

        with patch('src.actions.cardinal_list', test_cardinal_list):
            # Mock discord channel
            channel = AsyncMock()
            channel.send = AsyncMock()
            
            # Absolve the cardinal and check that the sin_coins were removed
            await absolve(member, channel)
            assert test_cardinal.sin_coins == 0
            #Check that the cardinal was mentioned
            assert channel.send.assert_called_once_with(f"<@{member.id}>, You have been absolved of all your sins!") == None


if __name__ == '__main__':
    unittest.main()