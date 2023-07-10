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


    async def test_print_standings(self):
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
        from src.actions import print_standings

        # Mock discord channel
        channel = AsyncMock()
        channel.send = AsyncMock()

        # Create a list of cardinals
        test_cardinal_list = []
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        test_cardinal = Cardinal(member)
        test_cardinal_list.append(test_cardinal)

        member = Mock()
        member.name = "Cardinal Test"
        test_cardinal = Cardinal(member)
        test_cardinal.add_pope_points(5)
        test_cardinal_list.append(test_cardinal)

        # Print standings and check that the channel was called
        with patch('src.utils.cardinal_list', test_cardinal_list):
            await print_standings(channel)
        assert channel.send.assert_called_once_with("Cardinal Test: 5\nTest Cardinal: 0") == None

    async def test_print_standings_with_empty_list(self):
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
        from src.actions import print_standings

        # Mock discord channel
        channel = AsyncMock()
        channel.send = AsyncMock()

        # Print standings and check that the channel was called
        with patch('src.utils.cardinal_list', []):
            await print_standings(channel)
        assert channel.send.assert_not_called() == None


    async def test_print_cardinals(self):
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
        from src.actions import print_cardinals

        # Mock discord channel
        channel = AsyncMock()
        channel.send = AsyncMock()

        # Create a list of cardinals
        test_cardinal_list = []
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        test_cardinal = Cardinal(member)
        test_cardinal_list.append(test_cardinal)

        member = Mock()
        member.name = "Cardinal Test"
        test_cardinal = Cardinal(member)
        test_cardinal_list.append(test_cardinal)

        # Print cardinals and check that the channel was called
        with patch('src.actions.cardinal_list', test_cardinal_list):
            await print_cardinals(channel)
        assert channel.send.assert_called_once_with("Cardinals:\nTest Cardinal\nCardinal Test") == None


    async def test_process_command_absolve_happy_pope_path(self):
        # Account for directory differences between test and src
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, check_for_pope_change
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].armageddon = False
        from src.actions import process_command

        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()
        mock_absolve = AsyncMock()
        mock_check_for_pope_change = AsyncMock()
        
        # Mock Pope role
        pope_role = Mock()
        pope_role.id = 9999
        pope_role.name = "Pope"
        
        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!ABSOLVE"
        message.channel = channel
        
        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        member.roles = [pope_role]
        
        # Append member to message
        message.author = member
        message.mentions = [member]
        
        with patch('src.actions.absolve', mock_absolve), patch('src.actions.check_for_pope_change', mock_check_for_pope_change):
            await process_command(message, client)
        assert mock_check_for_pope_change.assert_called_once_with(client) == None


    async def test_process_command_absolve_happy_path_not_pope(self):
        # Account for directory differences between test and src
        from src.cardinal import Cardinal
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, check_for_pope_change
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].armageddon = False
        from src.actions import process_command
        
        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()
        mock_absolve = AsyncMock()
        mock_check_for_pope_change = AsyncMock()
        
        # Mock Cardinal role
        cardinal_role = Mock()
        cardinal_role.id = 1111
        cardinal_role.name = "Cardinal"
        
        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!ABSOLVE"
        message.channel = channel
        
        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        member.roles = [cardinal_role]
        
        # Append member to message
        message.author = member
        message.mentions = [member]

        # Append member to cardinal list
        test_cardinal = Cardinal(member)
        test_cardinal_list = [test_cardinal]
        
        with patch('src.utils.cardinal_list', test_cardinal_list), \
        patch('src.actions.absolve', mock_absolve), \
        patch('src.actions.check_for_pope_change', mock_check_for_pope_change):
            await process_command(message, client)
        assert message.reply.assert_called_once_with("Only the Pope can absolve sins!") == None
        assert test_cardinal.popeliness() == -50
        assert mock_absolve.assert_not_called() == None
        assert mock_check_for_pope_change.assert_not_called() == None         


    async def test_process_command_absolve_pope_bad_mention(self):
        # Account for directory differences between test and src
        from src.cardinal import Cardinal
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, check_for_pope_change
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].armageddon = False
        from src.actions import process_command
        
        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()
        
        # Mock Cardinal role
        pope_role = Mock()
        pope_role.id = 9999
        pope_role.name = "Pope"
        
        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!ABSOLVE"
        message.channel = channel
        
        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        member.roles = [pope_role]
        
        # Append member to message
        message.author = member
        message.mentions = []
        
        await process_command(message, client)
        assert message.reply.assert_called_once_with("You need to mention someone to absolve them. Format: !Absolve @user") == None


    async def test_process_command_popeliness(self):
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
        from src.actions import process_command

        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()
        mock_print_standings = AsyncMock()
        message = AsyncMock()
        message.content = "!POPELINESS"
        message.channel = channel

        with patch('src.actions.print_standings', mock_print_standings):
            await process_command(message, client)
        assert mock_print_standings.assert_called_once_with(channel) == None

    async def test_process_command_armageddon(self):
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

        from src.actions import process_command
        
        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()
        message = AsyncMock()

        message.content = "!ARMAGEDDON"
        message.channel = channel

        await process_command(message, client)
        assert channel.send.assert_called_once_with("Armageddon has begun.") == None


    async def test_process_command_rapture_armageddon_not_active(self):
        # Account for directory differences between test and src
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, check_for_pope_change
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].armageddon = False
        from src.actions import process_command

        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()
        print = Mock()
        
        # Mock Pope role
        pope_role = Mock()
        pope_role.id = 9999
        pope_role.name = "Pope"
        
        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!RAPTURE"
        message.channel = channel
        
        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        member.roles = [pope_role]
        
        # Append member to message
        message.author = member
        message.mentions = [member]

        with patch('builtins.print', print):
            await process_command(message, client)
        assert print.assert_called_once_with("Error: Armageddon has not begun or author is not a pope") == None

    async def test_process_command_rapture_armageddon_not_pope(self):
        # Account for directory differences between test and src
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, check_for_pope_change
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].armageddon = True
        from src.actions import process_command

        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()
        print = Mock()
        
        # Mock Cardinal role
        cardinal_role = Mock()
        cardinal_role.id = 1111
        cardinal_role.name = "Cardinal"
        
        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!RAPTURE"
        message.channel = channel
        
        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        member.roles = [cardinal_role]
        
        # Append member to message
        message.author = member
        message.mentions = [member]

        with patch('builtins.print', print):
            await process_command(message, client)
        assert print.assert_called_once_with("Error: Armageddon has not begun or author is not a pope") == None


    async def test_process_command_rapture(self):
        # Account for directory differences between test and src
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, check_for_pope_change
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].armageddon = True
        from src.actions import process_command

        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()
        
        # Mock Pope role
        pope_role = Mock()
        pope_role.id = 9999
        pope_role.name = "Pope"
        
        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!RAPTURE"
        message.channel = channel
        
        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        member.roles = [pope_role]
        
        # Append member to message
        message.author = member
        message.mentions = [member]

        await process_command(message, client)
        assert channel.send.assert_called_once_with("Prepare for the Rapture!") == None


if __name__ == '__main__':
    unittest.main()