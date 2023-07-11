import sys
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock, patch

# Test Utils
class UtilsTests(IsolatedAsyncioTestCase):

    # Test Author is pope
    def test_author_is_pope_true(self):
        sys.modules['constants'] = Mock()
        sys.modules['constants'].POPE_ROLE_ID = "9999"
        sys.modules['cardinal'] = __import__('src.cardinal')
        from src.utils import author_is_pope, member_has_role

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
        from src.utils import author_is_pope, member_has_role

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
        from src.utils import author_is_pope, member_has_role

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
        from src.utils import author_is_pope, member_has_role

        #Mock a message with an Author
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890

        message = AsyncMock()
        message.author = member

        with self.assertRaises(Exception) as context:
            member_has_role(member, 8888)
        self.assertRaises(Exception)