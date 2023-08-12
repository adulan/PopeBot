import unittest, os, sys
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, Mock, patch
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
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
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
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"        
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
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
        with patch('src.utils.cardinal_list', test_cardinal_list), patch('discord.Embed', Mock()):
            await print_standings(channel)
        assert channel.send.assert_called_once() == None

    async def test_print_standings_with_empty_list(self):
        # Account for directory differences between test and src
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"        
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
        sys.modules['utils'].armageddon = False
        from src.actions import print_standings

        # Mock discord channel
        channel = AsyncMock()
        channel.send = AsyncMock()

        # Check that the channel was not called
        with patch('src.utils.cardinal_list', []):
            await print_standings(channel)
        assert channel.send.assert_not_called() == None


    async def test_print_cardinals(self):
        # Account for directory differences between test and src
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
        sys.modules['utils'].armageddon = False
        from src.actions import print_cardinals

        # Mock discord channel
        channel = AsyncMock()
        channel.send = AsyncMock()
        mock_embed = Mock()

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
        with patch('src.actions.cardinal_list', test_cardinal_list), patch('discord.Embed', mock_embed):
            await print_cardinals(channel)
        assert channel.send.assert_called_once() == None


    async def test_print_cardinals_with_empty_list(self):
        # Account for directory differences between test and src
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"        
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
        sys.modules['utils'].armageddon = False
        from src.actions import print_cardinals

        # Mock discord channel
        channel = AsyncMock()
        channel.send = AsyncMock()

        # Check that the channel was not called
        with patch('src.actions.cardinal_list', []):
            await print_cardinals(channel)
        assert channel.send.assert_not_called() == None

    async def test_process_command_absolve_happy_pope_path(self):
        # Account for directory differences between test and src
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"        
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
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
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"        
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
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
        assert test_cardinal.popeliness() == -500
        assert mock_absolve.assert_not_called() == None
        assert mock_check_for_pope_change.assert_not_called() == None         


    async def test_process_command_absolve_pope_bad_mention(self):
        # Account for directory differences between test and src
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"        
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
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
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
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
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list

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
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
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
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
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
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
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


    async def test_process_command_pope_points(self):
        # Account for directory differences between test and src
        from src.cardinal import Cardinal
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
        sys.modules['utils'].armageddon = False
        from src.actions import process_command
        
        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()
        mock_check_for_pope_change = AsyncMock()

        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!pp @TestCardinal 100"
        message.channel = channel

        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 2468101214

        message.mentions = [member]
        
        test_cardinal = Cardinal(member)
        test_cardinal_list = [test_cardinal]
        
        with patch('src.actions.check_for_pope_change', mock_check_for_pope_change), patch("src.utils.cardinal_list", test_cardinal_list):
            await process_command(message, client)
        assert mock_check_for_pope_change.assert_called_once_with(client) == None
        assert test_cardinal.pope_points == 100


    async def test_process_command_pope_points_max(self):
        # Account for directory differences between test and src
        from src.cardinal import Cardinal
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list,\
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
        sys.modules['utils'].armageddon = False
        from src.actions import process_command
        
        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()
        mock_check_for_pope_change = AsyncMock()

        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!pp @TestCardinal 10000000"
        message.channel = channel

        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 2468101214

        message.mentions = [member]
        message.author = member
        
        test_cardinal = Cardinal(member)
        test_cardinal.pope_points = 10
        test_cardinal.sin_coins = 10
        test_cardinal_list = [test_cardinal]
        
        with patch('src.actions.check_for_pope_change', mock_check_for_pope_change), patch("src.utils.cardinal_list", test_cardinal_list):
            await process_command(message, client)
        assert mock_check_for_pope_change.assert_called_once_with(client) == None
        assert test_cardinal.pope_points == 10
        assert test_cardinal.sin_coins == 35
        assert message.reply.assert_called_once_with("You can't give more than 1 million Pope Points at a time.") == None


    async def test_process_command_pope_points_self_punishment(self):
        # Account for directory differences between test and src
        from src.cardinal import Cardinal
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
        sys.modules['utils'].armageddon = False
        from src.actions import process_command
        
        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()
        mock_check_for_pope_change = AsyncMock()

        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!pp @TestCardinal 100"
        message.channel = channel

        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 2468101214
        member.roles = []

        message.mentions = [member]
        message.author = member
        
        test_cardinal = Cardinal(member)
        test_cardinal.pope_points = 10
        test_cardinal.sin_coins = 10
        test_cardinal_list = [test_cardinal]
        
        with patch('src.actions.check_for_pope_change', mock_check_for_pope_change), patch("src.utils.cardinal_list", test_cardinal_list):
            await process_command(message, client)
        assert mock_check_for_pope_change.assert_called_once_with(client) == None
        assert test_cardinal.pope_points == 110
        assert test_cardinal.sin_coins == 60


    async def test_process_command_pp_bad_mention(self):
        # Account for directory differences between test and src
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
        sys.modules['utils'].armageddon = False
        from src.actions import process_command
        
        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()

        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!pp @bad 0"
        message.channel = channel
        
        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890

        message.mentions = []
        
        await process_command(message, client)
        assert message.reply.assert_called_once_with("You need to mention someone to give them Pope Points. Format: !PP @user amount") == None


    async def test_process_command_pp_bad_format(self):
        # Account for directory differences between test and src
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
        sys.modules['utils'].armageddon = False
        from src.actions import process_command
        
        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()

        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!pp"
        message.channel = channel
        
        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890

        message.mentions = []
        
        await process_command(message, client)
        assert message.reply.assert_called_once_with("Format: !PP @user amount") == None


    async def test_process_command_pp_bad_amount(self):
        # Account for directory differences between test and src
        from src.cardinal import Cardinal
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
        sys.modules['utils'].armageddon = False
        from src.actions import process_command
        
        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()

        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!pp @TestCardinal a"
        message.channel = channel

        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 2468101214

        message.mentions = [member]
        
        test_cardinal = Cardinal(member)
        test_cardinal_list = [test_cardinal]        
        
        with patch('src.utils.cardinal_list', test_cardinal_list):
            await process_command(message, client)
        assert message.reply.assert_called_once_with("You need to enter a number. Format: !PP @user amount") == None


    async def test_process_command_pope_points_bad_cardinal(self):
        # Account for directory differences between test and src
        from src.cardinal import Cardinal
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
        sys.modules['utils'].armageddon = False
        from src.actions import process_command
        
        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()
        mock_check_for_pope_change = AsyncMock()
        mock_print = Mock()

        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!pp @TestCardinal 100"
        message.channel = channel

        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 2468101214

        message.mentions = [member]
        
        test_cardinal = Cardinal(member)
        test_cardinal.id = 1111111111
        test_cardinal_list = [test_cardinal]
        
        with patch('src.actions.check_for_pope_change', mock_check_for_pope_change), patch("src.utils.cardinal_list", test_cardinal_list), \
            patch("builtins.print", mock_print):
            await process_command(message, client)
        assert mock_check_for_pope_change.assert_not_called() == None
        assert mock_print.assert_called_once_with("Cardinal not found") == None


    async def test_process_command_sin_coins(self):
        # Account for directory differences between test and src
        from src.cardinal import Cardinal
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            set_mention_cardinals, check_for_pope_change, save_cardinals_json
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
        sys.modules['utils'].armageddon = False
        from src.actions import process_command
        
        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()
        mock_check_for_pope_change = AsyncMock()
        
        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!Sin @TestCardinal 50"
        message.channel = channel

        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 2468101214

        message.mentions = [member]
        
        test_cardinal = Cardinal(member)
        test_cardinal_list = [test_cardinal]
        
        with patch('src.actions.check_for_pope_change', mock_check_for_pope_change), patch("src.utils.cardinal_list", test_cardinal_list):
            await process_command(message, client)
        assert mock_check_for_pope_change.assert_called_once_with(client) == None
        assert test_cardinal.sin_coins == 50


    async def test_process_command_sin_coins_max(self):
        # Account for directory differences between test and src
        from src.cardinal import Cardinal
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            set_mention_cardinals, check_for_pope_change, save_cardinals_json
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
        sys.modules['utils'].armageddon = False
        from src.actions import process_command
        
        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()
        mock_check_for_pope_change = AsyncMock()
        
        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!Sin @TestCardinal 10000000"
        message.channel = channel

        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 2468101214

        message.mentions = [member]
        message.author = member
        
        test_cardinal = Cardinal(member)
        test_cardinal.pope_points = 10
        test_cardinal.sin_coins = 10
        test_cardinal_list = [test_cardinal]
        
        with patch('src.actions.check_for_pope_change', mock_check_for_pope_change), patch("src.utils.cardinal_list", test_cardinal_list):
            await process_command(message, client)
        assert mock_check_for_pope_change.assert_called_once_with(client) == None
        assert test_cardinal.sin_coins == 1000010
        assert message.reply.assert_called_once_with("You can't give more than 1 million Sin Coins at a time.") == None


    async def test_process_command_sc_bad_mention(self):
        # Account for directory differences between test and src
        from src.cardinal import Cardinal
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
        sys.modules['utils'].armageddon = False
        from src.actions import process_command
        
        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()
        
        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!siN @bad 0"
        message.channel = channel
        
        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890

        message.mentions = []
        
        await process_command(message, client)
        assert message.reply.assert_called_once_with("You need to mention someone to give them Sin Coins. Format: !SIN @user amount") == None


    async def test_process_command_sc_bad_format(self):
        # Account for directory differences between test and src
        from src.cardinal import Cardinal
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
        sys.modules['utils'].armageddon = False
        from src.actions import process_command
        
        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()
        
        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!sin"
        message.channel = channel
        
        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        
        message.mentions = []
        
        await process_command(message, client)
        assert message.reply.assert_called_once_with("Format: !SIN @user amount") == None


    async def test_process_command_sc_bad_amount(self):
        # Account for directory differences between test and src
        from src.cardinal import Cardinal
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
        sys.modules['utils'].armageddon = False
        from src.actions import process_command
        
        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()
                
        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!SIN @TestCardinal a"
        message.channel = channel

        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 2468101214
        
        message.mentions = [member]
        
        test_cardinal = Cardinal(member)
        test_cardinal_list = [test_cardinal]        
        
        with patch('src.utils.cardinal_list', test_cardinal_list):
            await process_command(message, client)
        assert message.reply.assert_called_once_with("You need to enter a number. Format: !SIN @user amount") == None

    async def test_process_command_sc_bad_cardinal(self):
        # Account for directory differences between test and src
        from src.cardinal import Cardinal
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].POPE_ROLE_ID = 9999
        sys.modules['constants'].CARDINAL_ROLE_ID = 1234567890
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        sys.modules['cardinal'] = __import__('src.cardinal')
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['utils'].cardinal_list = ['']
        from src.utils import author_is_pope, get_cardinal_by_id, rank_cardinals, add_member_to_cardinal_list, \
            check_for_pope_change, save_cardinals_json, populate_cardinals_json, set_mention_cardinals
        sys.modules['utils'].set_mention_cardinals = set_mention_cardinals
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        sys.modules['utils'].author_is_pope = author_is_pope
        sys.modules['utils'].get_cardinal_by_id = get_cardinal_by_id
        sys.modules['utils'].rank_cardinals = rank_cardinals
        sys.modules['utils'].check_for_pope_change = check_for_pope_change
        sys.modules['utils'].add_member_to_cardinal_list = add_member_to_cardinal_list
        sys.modules['utils'].armageddon = False
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        from src.actions import process_command
        
        # Mock discord objects
        client = AsyncMock()
        channel = AsyncMock()
        mock_check_for_pope_change = AsyncMock()
        mock_print = Mock()

        # Mock message
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!sin @TestCardinal 100"
        message.channel = channel

        # Mock discord member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 2468101214

        message.mentions = [member]
        
        test_cardinal = Cardinal(member)
        test_cardinal.id = 1111111111
        test_cardinal_list = [test_cardinal]
        
        with patch('src.actions.check_for_pope_change', mock_check_for_pope_change), patch("src.utils.cardinal_list", test_cardinal_list), \
            patch("builtins.print", mock_print):
            await process_command(message, client)
        assert mock_check_for_pope_change.assert_not_called() == None
        assert mock_print.assert_called_once_with("Cardinal not found") == None


    async def test_process_command_cardinals(self):
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        from src.actions import process_command

        # Mock message
        channel = AsyncMock()
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!cardinals"
        message.channel = channel

        mock_print_cardinals = AsyncMock()
        mock_client = AsyncMock()
        with patch('src.actions.print_cardinals', mock_print_cardinals):
            await process_command(message, mock_client)
        assert mock_print_cardinals.assert_called_once_with(channel) == None

    
    async def test_process_command_help(self):
        sys.modules['bible_verses'] = Mock()
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        from src.actions import process_command
        mock_embeds = Mock()

        # Mock message
        channel = AsyncMock()
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!pope-help"
        message.channel = channel

        mock_client = AsyncMock()
        with patch('discord.Embed', Mock(return_value=mock_embeds)):
            await process_command(message, mock_client)
        
        assert message.channel.send.assert_called_once() == None
        assert mock_embeds.add_field.call_count == 7

    
    async def test_process_command_save(self):
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        sys.modules['bible_verses'] = Mock()
        from src.utils import save_cardinals_json
        from src.actions import process_command
        sys.modules['utils'].save_cardinals_json = save_cardinals_json
        
        mock_client = AsyncMock()
        mock_save = MagicMock()

        # Mock message
        channel = AsyncMock()
        message = AsyncMock()
        message.reply = AsyncMock()
        message.content = "!save"
        message.channel = channel

        with patch('src.actions.save_cardinals_json', mock_save):
            await process_command(message, mock_client)
        assert mock_save.assert_called_once() == None
        assert message.reply.assert_called_once_with("Cardinals saved") == None


    async def test_process_command_load(self):
        sys.modules['bible_verses'] = Mock()
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        from src.utils import populate_cardinals_json
        from src.actions import process_command
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        
        mock_client = AsyncMock()
        mock_load = MagicMock()
        channel = MagicMock()

        # Mock discord member
        member1 = Mock()
        member1.name = "Test Cardinal 1"
        member1.id = 1234567890

        # Mock discord member
        member2 = Mock()
        member2.name = "Test Cardinal 2"
        member2.id = 2468101214

        # Mock message
        message1 = MagicMock()
        message1.reply = AsyncMock()
        message1.content = "!load"
        message1.channel = channel
        message1.author = member1

        # Mock message
        message2 = MagicMock()
        message2.reply = AsyncMock()
        message2.content = "!load"
        message2.channel = channel
        message2.author = member2

        channel.history.return_value = AsyncIterator(message1, message2)
        
        with patch('src.actions.populate_cardinals_json', mock_load):
            await process_command(message1, mock_client)
        assert mock_load.assert_called_once() == None
        assert message1.reply.assert_called_once_with("Cardinals loaded") == None


    async def test_process_command_load_not_double(self):
        sys.modules['bible_verses'] = Mock()
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        from src.utils import populate_cardinals_json
        from src.actions import process_command
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        
        mock_client = AsyncMock()
        mock_load = MagicMock()
        channel = MagicMock()
        mock_print = Mock()

        # Mock discord member
        member1 = Mock()
        member1.name = "Test Cardinal 1"
        member1.id = 1234567890

        # Mock discord member
        member2 = Mock()
        member2.name = "Test Cardinal 2"
        member2.id = 2468101214

        # Mock message
        message1 = MagicMock()
        message1.reply = AsyncMock()
        message1.content = "!load"
        message1.channel = channel
        message1.author = member1

        # Mock message
        message2 = MagicMock()
        message2.reply = AsyncMock()
        message2.content = "!test"
        message2.channel = channel
        message2.author = member2

        channel.history.return_value = AsyncIterator(message1, message2)
        
        with patch('src.actions.populate_cardinals_json', mock_load), patch('builtins.print', mock_print):
            await process_command(message1, mock_client)
        assert mock_load.assert_not_called() == None
        assert message1.reply.assert_not_called() == None
        assert mock_print.assert_called_once_with("Need two members to load Cardinals") == None


    async def test_process_command_load_same_author(self):
        sys.modules['bible_verses'] = Mock()
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        from src.utils import populate_cardinals_json
        from src.actions import process_command
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        
        mock_client = AsyncMock()
        mock_load = MagicMock()
        channel = MagicMock()
        mock_print = Mock()

        # Mock discord member
        member1 = Mock()
        member1.name = "Test Cardinal 1"
        member1.id = 1234567890

        # Mock discord member
        member2 = Mock()
        member2.name = "Test Cardinal 2"
        member2.id = 2468101214

        # Mock message
        message1 = MagicMock()
        message1.reply = AsyncMock()
        message1.content = "!load"
        message1.channel = channel
        message1.author = member1

        # Mock message
        message2 = MagicMock()
        message2.reply = AsyncMock()
        message2.content = "!load"
        message2.channel = channel
        message2.author = member1

        channel.history.return_value = AsyncIterator(message1, message2)
        
        with patch('src.actions.populate_cardinals_json', mock_load), patch('builtins.print', mock_print):
            await process_command(message1, mock_client)
        assert mock_load.assert_not_called() == None
        assert message1.reply.assert_not_called() == None
        assert mock_print.assert_called_once_with("Need two members to load Cardinals") == None


    async def test_process_command_load_no_json(self):
        sys.modules['bible_verses'] = Mock()
        sys.modules['utils'] = __import__('src.utils')
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['constants'].CARDINAL_LIST_FILE = "test_cardinals.json"
        from src.utils import populate_cardinals_json
        from src.actions import process_command
        sys.modules['utils'].populate_cardinals_json = populate_cardinals_json
        
        mock_client = AsyncMock()
        mock_load = MagicMock()
        mock_load.return_value = False
        channel = MagicMock()
        mock_print = Mock()

        # Mock discord member
        member1 = Mock()
        member1.name = "Test Cardinal 1"
        member1.id = 1234567890

        # Mock discord member
        member2 = Mock()
        member2.name = "Test Cardinal 2"
        member2.id = 2468101214

        # Mock message
        message1 = MagicMock()
        message1.reply = AsyncMock()
        message1.content = "!load"
        message1.channel = channel
        message1.author = member1

        # Mock message
        message2 = MagicMock()
        message2.reply = AsyncMock()
        message2.content = "!load"
        message2.channel = channel
        message2.author = member2

        channel.history.return_value = AsyncIterator(message1, message2)
        
        with patch('src.actions.populate_cardinals_json', mock_load), patch('builtins.print', mock_print):
            await process_command(message1, mock_client)
        assert mock_load.assert_called_once() == None
        assert message1.reply.assert_not_called() == None
        assert mock_print.assert_called_once_with("Error: Could not load Cardinals") == None


    async def test_process_command_mention_true(self):
        from src.actions import process_command
        sys.modules['bible_verses'] = Mock()

        # Mock message
        message1 = MagicMock()
        message1.reply = AsyncMock()
        message1.content = "!Mention True"

        mock_mention = Mock()
        mock_print = Mock()

        with patch('src.actions.set_mention_cardinals', mock_mention), patch('builtins.print', mock_print):
            await process_command(message1, None)
        assert mock_mention.assert_called_once_with(True) == None
        assert mock_print.assert_called_once_with("Mentioning Cardinals during Habemus Papam") == None


    async def test_process_command_mention_false(self):
        from src.actions import process_command
        sys.modules['bible_verses'] = Mock()
        # Mock message
        message1 = MagicMock()
        message1.reply = AsyncMock()
        message1.content = "!Mention False"

        mock_mention = Mock()
        mock_print = Mock()

        with patch('src.actions.set_mention_cardinals', mock_mention), patch('builtins.print', mock_print):
            await process_command(message1, None)
        assert mock_mention.assert_called_once_with(False) == None
        assert mock_print.assert_called_once_with("Habemus Papam will not mention Cardinals") == None


    async def test_process_command_mention_bad_command(self):
        from src.actions import process_command
        
        # Mock message
        message1 = MagicMock()
        message1.reply = AsyncMock()
        message1.content = "!Mention"

        mock_mention = Mock()
        mock_print = Mock()

        with patch('src.actions.set_mention_cardinals', mock_mention), patch('builtins.print', mock_print):
            await process_command(message1, None)
        assert message1.reply.assert_called_once_with("Format: !Mention [True|False]") == None

    
    async def test_process_command_add_cardinal(self):
        from src.actions import process_command
        sys.modules['bible_verses'] = Mock()

        # Mock discord member
        member1 = Mock()
        member1.name = "Test Cardinal 1"
        member1.id = 1234567890

        # Mock message
        message1 = MagicMock()
        message1.reply = AsyncMock()
        message1.content = "!add-cardinal @TestCardinal"
        message1.mentions = [member1]

        mock_add_cardinal = Mock()

        with patch('src.actions.add_member_to_cardinal_list', mock_add_cardinal):
            await process_command(message1, None)
        assert mock_add_cardinal.assert_called_once() == None
        assert message1.reply.assert_called_once_with("Test Cardinal 1 added to Cardinals") == None


    async def test_process_command_add_cardinal_false(self):
        from src.actions import process_command
        sys.modules['bible_verses'] = Mock()

        # Mock discord member
        member1 = Mock()
        member1.name = "Test Cardinal 1"
        member1.id = 1234567890
        
        # Mock message
        message1 = MagicMock()
        message1.reply = AsyncMock()
        message1.content = "!add-cardinal @TestCardinal"
        message1.mentions = [member1]

        mock_add_cardinal = Mock()
        mock_add_cardinal.return_value = False

        with patch('src.actions.add_member_to_cardinal_list', mock_add_cardinal):
            await process_command(message1, None)
        assert mock_add_cardinal.assert_called_once() == None
        assert message1.reply.assert_called_once_with("Test Cardinal 1 already a Cardinal") == None


if __name__ == '__main__':
    unittest.main()

class AsyncIterator:
    def __init__(self, *args):
        self.args = args
        self.index = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.index < len(self.args):
            result = self.args[self.index]
            self.index += 1
            return result
        else:
            raise StopAsyncIteration