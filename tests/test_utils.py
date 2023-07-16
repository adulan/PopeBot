import sys
from unittest import IsolatedAsyncioTestCase
import unittest
from unittest.mock import AsyncMock, MagicMock, Mock, patch, mock_open

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


    # Test announce_pope_change
    async def test_announce_pope_change(self):
        sys.modules['constants'] = AsyncMock()
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

        assert await announce_pope_change(member, mock_client) == None
        assert mock_channel.send.assert_called_once_with("@Test Pope is the New Pope!") == None


if __name__ == '__main__':
    unittest.main()