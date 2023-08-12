import sys, os
from unittest import IsolatedAsyncioTestCase
import unittest
from unittest.mock import AsyncMock, MagicMock, Mock, patch, mock_open

import discord

# Test Utils
class UtilsTests(IsolatedAsyncioTestCase):
    
    def setUp(self):
        #Suppress print statements
        import sys
        sys.stdout = open(os.devnull, 'w')
        
        #Suppress warnings
        import warnings
        warnings.filterwarnings("ignore")
    
    
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
        member = MagicMock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        member.roles = None

        message = AsyncMock()
        message.author = member
        mock_print = Mock()

        assert member_has_role(member, 8888) == False


    # Test save cardinals json
    def test_save_cardinals_json(self):
        from src.utils import save_cardinals_json
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
        json_mock = Mock()
        expected_json_output = [{'name': 'Test Cardinal', 'id': 1234567890, 'pope_points': 0, 'sin_coins': 0}]

        with patch('src.utils.cardinal_list', test_cardinal_list), patch('builtins.print', print_mock), patch('json.dump', json_mock):
            with patch('builtins.open', mock_open(read_data="data")) as mock_file:
                save_cardinals_json()
        
        # Check that the file was opened and written to with JSON
        mock_file.assert_called_once()
        json_mock.assert_called_once_with(expected_json_output, mock_file())
        assert print_mock.assert_called_once_with("Cardinals saved.") == None


    def test_save_cardinals_json_exception(self):
        from src.utils import save_cardinals_json
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
        json_mock = Mock()

        with patch('src.utils.cardinal_list', test_cardinal_list), patch('builtins.print', print_mock), patch('json.dump', json_mock):
            with patch('builtins.open', Exception):
                self.assertRaises(Exception,  save_cardinals_json())
    
        json_mock.assert_not_called()
        self.assertEqual(print_mock.call_count, 2)

    
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

    
    # Test get_cardinal_by_id empty list
    def test_get_cardinal_by_id_none(self):
        sys.modules['cardinal'] = __import__('src.cardinal')
        from src.utils import get_cardinal_by_id

        with patch('src.utils.cardinal_list', []):
            assert get_cardinal_by_id(1234567890) == None


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


    def test_get_member_from_cardinal_list_none(self):
        sys.modules['cardinal'] = __import__('src.cardinal')
        from src.utils import get_member_from_cardinal_list
        from src.cardinal import Cardinal

        # Mock a member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890

        test_cardinal_list = [] 

        with patch('src.utils.cardinal_list', test_cardinal_list):
            assert get_member_from_cardinal_list(member) == None


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

    
    # Test rank_cardinals
    def test_rank_cardinals(self):
        from src.cardinal import Cardinal
        from src.utils import rank_cardinals

        # Mock a member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890

        # Mock a member
        member2 = Mock()
        member2.name = "Test Cardinal 2"
        member2.id = 9876543210

        # Mock a member
        member3 = Mock()
        member3.name = "Test Cardinal 3"
        member3.id = 2468101214

        # Mock a member
        member4 = Mock()
        member4.name = "Test Cardinal 4"
        member4.id = 3691215182

        # Mock a member
        member5 = Mock()
        member5.name = "Test Cardinal 5"
        member5.id = 4812162024

        # Create cardinals from mock members
        test_cardinal = Cardinal(member)
        test_cardinal2 = Cardinal(member2)
        test_cardinal3 = Cardinal(member3)
        test_cardinal4 = Cardinal(member4)
        test_cardinal5 = Cardinal(member5)

        # Set pope_points
        test_cardinal.pope_points = 10
        test_cardinal2.pope_points = 40
        test_cardinal3.pope_points = 15
        test_cardinal4.pope_points = 20
        test_cardinal5.pope_points = 15

        # Set sin_coins 
        test_cardinal.sin_coins = 0
        test_cardinal2.sin_coins = 1
        test_cardinal3.sin_coins = 25
        test_cardinal4.sin_coins = 5
        test_cardinal5.sin_coins = 0

        # Add cardinals to list
        test_cardinal_list = [test_cardinal, test_cardinal2, test_cardinal3, test_cardinal4, test_cardinal5]

        with patch('src.utils.cardinal_list', test_cardinal_list):
            assert rank_cardinals() == [test_cardinal2, test_cardinal5, test_cardinal, test_cardinal4, test_cardinal3]


    # Test check_for_pope_change
    async def test_check_for_pope_change(self):
        from src.cardinal import Cardinal
        from src.utils import check_for_pope_change

        # Mock Pope role
        pope_role = AsyncMock()
        pope_role.id = 9999
        pope_role.name = "Pope"

        # Mock Cardinal role
        cardinal_role = AsyncMock()
        cardinal_role.id = 8888
        cardinal_role.name = "Cardinal"
        
        # Mock a member
        member = AsyncMock()
        member.name = "Test Pope"
        member.id = 1234567890
        member.roles = [pope_role]

        # Mock a member
        member2 = AsyncMock()
        member2.name = "Test Cardinal"
        member2.id = 9876543210
        member2.roles = [cardinal_role]

        # Add mocks to cardinal_list
        test_pope = Cardinal(member)
        test_pope.pope_points = 10
        test_cardinal = Cardinal(member2)
        test_cardinal.pope_points = 40
        test_cardinal_list = [test_pope, test_cardinal]

        mock_client = AsyncMock()
        mock_set_pope = AsyncMock()
        mock_get_pope = MagicMock(return_value = test_pope)

        with patch("src.utils.cardinal_list", test_cardinal_list), patch("src.utils.get_pope", mock_get_pope), patch("src.utils.set_pope", mock_set_pope):
            assert await check_for_pope_change(mock_client) == True
        assert mock_set_pope.assert_called_once_with(member2, member, mock_client) == None


     # Test check_for_pope_change
    async def test_check_for_pope_change_no_cardinals(self):
        from src.utils import check_for_pope_change

        mock_client = AsyncMock()
        mock_set_pope = AsyncMock()
        mock_get_pope = MagicMock(return_value = None)

        with patch("src.utils.cardinal_list", []), patch("src.utils.get_pope", mock_get_pope), patch("src.utils.set_pope", mock_set_pope):
            assert await check_for_pope_change(mock_client) == False
        assert mock_set_pope.assert_not_called() == None


    # Test check_for_pope_change
    async def test_check_for_pope_change_no_pope(self):
        from src.cardinal import Cardinal
        from src.utils import check_for_pope_change

        # Mock Pope role
        pope_role = AsyncMock()
        pope_role.id = 9999
        pope_role.name = "Pope"

        # Mock Cardinal role
        cardinal_role = AsyncMock()
        cardinal_role.id = 8888
        cardinal_role.name = "Cardinal"
        
        # Mock a member
        member = AsyncMock()
        member.name = "Test Pope"
        member.id = 1234567890
        member.roles = [cardinal_role]

        # Mock a member
        member2 = AsyncMock()
        member2.name = "Test Cardinal"
        member2.id = 9876543210
        member2.roles = [cardinal_role]

        # Add mocks to cardinal_list
        test_cardinal = Cardinal(member)
        test_cardinal.pope_points = 10
        test_cardinal2 = Cardinal(member2)
        test_cardinal2.pope_points = 40
        test_cardinal_list = [test_cardinal, test_cardinal2]

        mock_client = AsyncMock()
        mock_set_pope = AsyncMock()

        with patch("src.utils.cardinal_list", test_cardinal_list), patch("src.utils.set_pope", mock_set_pope):
            assert await check_for_pope_change(mock_client) == True
        assert mock_set_pope.assert_called_once_with(member2, None, mock_client) == None


    # Test set_pope
    async def test_set_pope(self):
        from src.cardinal import Cardinal
        from src.utils import set_pope

        mock_add_roles = AsyncMock()
        mock_remove_roles = AsyncMock()

        # Mock Pope role
        pope_role = AsyncMock()
        pope_role.id = 9999
        pope_role.name = "Pope"

        # Mock Cardinal role
        cardinal_role = AsyncMock()
        cardinal_role.id = 8888
        cardinal_role.name = "Cardinal"
        
        # Mock a member
        member = AsyncMock()
        member.name = "Test Pope"
        member.id = 1234567890
        member.roles = [cardinal_role]
        member.add_roles = mock_add_roles
        member.remove_roles = mock_remove_roles

        # Mock a member
        member2 = AsyncMock()
        member2.name = "Test Cardinal"
        member2.id = 9876543210
        member2.roles = [cardinal_role]
        member2.add_roles = mock_add_roles
        member2.remove_roles = mock_remove_roles

        # Add mocks to cardinal_list
        test_cardinal = Cardinal(member)
        test_cardinal.pope_points = 10
        test_cardinal2 = Cardinal(member2)
        test_cardinal2.pope_points = 40
        test_cardinal_list = [test_cardinal, test_cardinal2]

        mock_client = AsyncMock()
        mock_client.get_guild = MagicMock()
        mock_guild = AsyncMock()
        mock_guild.get_role = MagicMock(return_value = pope_role)
        mock_client.get_guild.return_value = mock_guild

        mock_announce = AsyncMock()
        mock_save_cardinals = MagicMock(return_value = None)

        with patch("src.utils.cardinal_list", test_cardinal_list), patch("src.utils.get_pope", MagicMock(return_value = test_cardinal)), \
             patch("src.utils.announce_pope_change", mock_announce), patch("src.utils.save_cardinals_json", mock_save_cardinals):
            assert await set_pope(member2, member, mock_client) == True
        assert mock_add_roles.assert_called_once_with(pope_role) == None
        assert mock_remove_roles.assert_called_once_with(pope_role) == None
        assert mock_announce.assert_called_once_with(member2, mock_client) == None
        assert mock_save_cardinals.assert_called_once() == None


    async def test_set_pope_exception(self):
        from src.utils import set_pope
        
        # # Mock a member
        member = AsyncMock()
        member2 = AsyncMock()

        mock_exception = MagicMock(side_effect = discord.DiscordException)
        mock_client = AsyncMock()
        mock_client.get_guild = mock_exception
        mock_print = MagicMock()

        with patch('discord.DiscordException', mock_exception), patch('builtins.print', mock_print):
            await set_pope(member2, member, mock_client)
        assert mock_exception.assert_called_once() == None
        self.assertTrue(mock_print.called, 2)


    # Test announce_pope_change
    async def test_announce_pope_change(self):
        sys.modules['constants'] = Mock()
        sys.modules['utils'].CARDINAL_ROLE_ID = "9999"
        sys.modules['utils'].HABEMUS_IMAGE_FILE = "/test/image.png"
        sys.modules['utils'].WHITE_SMOKE_FILE = "/test/image.png"
        sys.modules['utils'].BLACK_SMOKE_FILE = "/test/black.png"
        sys.modules['utils'].ANNOUNCEMENT_CHANNEL_ID = "9999"
        sys.modules['cardinal'] = AsyncMock()
        from src.utils import announce_pope_change

        # Mock Pope role
        pope_role = AsyncMock()
        pope_role.id = 9999
        pope_role.name = "Pope"
        
        # Mock a member
        member = AsyncMock()
        member.name = "Test Pope"
        member.id = 1234567890
        member.roles = [pope_role]
        member.mention = "@Test Pope"

        mock_channel = AsyncMock()
        mock_client = AsyncMock()
        mock_client.get_channel = MagicMock(return_value = mock_channel)
        mock_client.get_channel.return_value = mock_channel
        mock_change = AsyncMock()
        mock_image = AsyncMock()

        with patch("src.utils.change_guild_icon", mock_change), patch('discord.File', MagicMock(return_value= mock_image)), \
            patch("asyncio.sleep", MagicMock(return_value = None)):
            await announce_pope_change(member, mock_client)
        assert mock_channel.send.assert_called_once_with("Habemus Papam!\n@Test Pope is the new pope!", file=mock_image) == None
        self.assertTrue(mock_change.call_count, 2)


    async def test_announce_pope_change_mentions(self):
        sys.modules['constants'] = Mock()
        sys.modules['utils'].CARDINAL_ROLE_ID = "9999"
        sys.modules['utils'].HABEMUS_IMAGE_FILE = "/test/image.png"
        sys.modules['utils'].WHITE_SMOKE_FILE = "/test/image.png"
        sys.modules['utils'].ANNOUNCEMENT_CHANNEL_ID = "9999"
        sys.modules['cardinal'] = AsyncMock()
        from src.utils import announce_pope_change

        # Mock Pope role
        pope_role = AsyncMock()
        pope_role.id = 9999
        pope_role.name = "Pope"
        
        # Mock a member
        member = AsyncMock()
        member.name = "Test Pope"
        member.id = 1234567890
        member.roles = [pope_role]
        member.mention = "@Test Pope"

        mock_channel = AsyncMock()
        mock_client = AsyncMock()
        mock_client.get_channel = MagicMock(return_value = mock_channel)
        mock_client.get_channel.return_value = mock_channel
        mock_change = AsyncMock()
        mock_image = AsyncMock()

        with patch("src.utils.change_guild_icon", mock_change), patch('discord.File', MagicMock(return_value= mock_image)), \
            patch("src.utils.mention_cardinals", MagicMock(return_value = True)), patch("asyncio.sleep", MagicMock(return_value = None)):
            await announce_pope_change(member, mock_client)
        assert mock_channel.send.assert_called_once_with("<@&9999> Habemus Papam!\n@Test Pope is the new pope!", file=mock_image) == None
        self.assertTrue(mock_change.call_count, 2)
   
   
    async def test_announce_pope_change_exception(self):
        from src.utils import announce_pope_change
        
        # # Mock a member
        member = AsyncMock()
        member.name = "Test Pope"
        member.id = 1234567890
        member.mention = "@Test Pope"

        mock_channel = AsyncMock()
        mock_channel.send = Exception

        mock_client = AsyncMock()
        mock_client.get_channel = mock_channel
        mock_print = MagicMock()

        with patch('builtins.print', mock_print), patch("asyncio.sleep", MagicMock(return_value = None)):
            self.assertRaises(Exception, await announce_pope_change(member, mock_client))
        assert mock_client.get_channel.assert_called_once() == None
        self.assertEqual(mock_print.call_count, 4)


    # Test populate cardinals
    async def test_populate_cardinals_no_file(self):
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

        mock_client = MagicMock()
        mock_guild = MagicMock()
        mock_guild.members.return_value = [member]
        mock_guild.get_role.return_value = cardinal_role
        mock_client.get_guild.return_value = mock_guild

        cardinal_mock = Mock(return_value=test_cardinal)
        
        from_json_mock = MagicMock(return_value=True)
        from_json_mock.from_json.return_value = test_cardinal
        cardinal_mock.from_json = Mock()

        with patch('src.utils.cardinal_list', test_cardinal_list),  patch('json.load', json_mock):
            with  patch('builtins.print', print_mock), patch('os.path.isfile', MagicMock(return_value=False)):
                await populate_cardinals(mock_client)
        
        # Check that two messages were printed
        # print("No cardinal_list.json found. Populating from guild.")
        # print("Cardinals populated.")
        self.assertEqual(print_mock.call_count, 2)


    async def test_populate_cardinals_happy(self):
        sys.modules['utils'].GUILD_ID = 1234567890
        sys.modules['utils'].CARDINAL_ROLE_ID = 1111
        sys.modules['cardinal'].Cardinal = Mock()
        from src.utils import populate_cardinals
        from src.cardinal import Cardinal

        # Mock Cardinal role
        cardinal_role = Mock()
        cardinal_role.id = 1111
        cardinal_role.name = "Cardinal"

        # Mock a member
        member = AsyncMock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        member.roles = []
        member.bot = False

        # Mock a member
        member2 = AsyncMock()
        member2.name = "Test Cardinal 2"
        member2.id = 2468101214
        member2.roles = [cardinal_role]
        member2.bot = False

        # Add mock to cardinal_list
        test_cardinal = Cardinal(member)
        test_cardinal_list = [test_cardinal] 

        # Mocks to capture function calls
        print_mock = Mock()
        populate_cardinals_mock = Mock(return_value=True)
        check_pope_change_mock = AsyncMock()

        mock_client = MagicMock()
        mock_guild = MagicMock()
        mock_guild.members = [member, member2]
        mock_guild.get_role.return_value = cardinal_role
        mock_client.get_guild.return_value = mock_guild

        cardinal_mock = Mock(return_value=test_cardinal)
        
        from_json_mock = MagicMock(return_value=True)
        from_json_mock.from_json.return_value = test_cardinal
        cardinal_mock.from_json = Mock()

        with patch('src.utils.cardinal_list', test_cardinal_list),  patch('os.path.isfile', MagicMock(return_value=True)), patch('src.utils.populate_cardinals_json', populate_cardinals_mock):
            with  patch('builtins.print', print_mock), patch('src.utils.check_for_pope_change', check_pope_change_mock):
                await populate_cardinals(mock_client)
        
        assert populate_cardinals_mock.assert_called_once() == None
        assert check_pope_change_mock.assert_called_once() == None
        self.assertTrue(print_mock.call_count, 2)


    async def test_change_guild_icon(self):
        sys.modules['utils'].GUILD_ID = 1234567890
        from src.utils import change_guild_icon

        mock_client = MagicMock()
        mock_guild = MagicMock()
        mock_client.get_guild.return_value = mock_guild
        mock_image = AsyncMock()

        with patch('builtins.open', mock_open(read_data="icon")) as mock_file:
            await change_guild_icon(mock_client, mock_image)
        assert mock_guild.edit.assert_called_once_with(icon="icon") == None
        assert mock_file.assert_called_once_with(mock_image, 'rb') == None

    async def test_change_guild_icon_exception(self):
        sys.modules['utils'].GUILD_ID = 1234567890
        from src.utils import change_guild_icon
        
        mock_client = MagicMock()
        mock_guild = MagicMock()
        mock_client.get_guild.return_value = mock_guild

        mock_image = AsyncMock()
        mock_print = Mock()

        with patch('builtins.print', mock_print):
            self.assertRaises(Exception, await change_guild_icon(mock_client, mock_image))
        self.assertTrue(mock_print.call_count, 2) == None


    def test_get_habemus_image(self):
        sys.modules['utils'].HABEMUS_IMAGE_PATH = "test/image.png"
        from src.utils import get_habemus_image

        with patch('builtins.open', mock_open(read_data="icon")) as mock_file:
            assert get_habemus_image() == "icon"
        assert mock_file.assert_called_once_with('/test/image.png', 'rb') == None

    
    def test_get_habemus_image_exception(self):
        sys.modules['utils'].HABEMUS_IMAGE_PATH = "test/image.png"
        from src.utils import get_habemus_image

        mock_print = Mock()

        with patch('builtins.print', mock_print):
            self.assertRaises(Exception, get_habemus_image())
        self.assertTrue(mock_print.call_count, 2) == None


    def test_set_mention_cardinals(self):
        from src.utils import set_mention_cardinals
        
        set_mention_cardinals(True)
        from src.utils import mention_cardinals
        self.assertTrue(mention_cardinals, True)

        set_mention_cardinals(False)
        from src.utils import mention_cardinals
        assert mention_cardinals == False


    def test_add_member_to_cardinal_list(self):
        from src.utils import add_member_to_cardinal_list
        from src.cardinal import Cardinal
        sys.modules['cardinal'].Cardinal = Cardinal

        # Mock a member
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        member.bot = False

        # Add mock to cardinal_list
        
        test_cardinal_list = []

        mock_get_member = Mock(return_value=None)

        with patch('src.utils.cardinal_list', test_cardinal_list), patch('src.utils.get_member_from_cardinal_list', mock_get_member):
            add_member_to_cardinal_list(member)
        assert len(test_cardinal_list) == 1
        assert mock_get_member.assert_called_once_with(member) == None
        
if __name__ == '__main__':
    unittest.main()