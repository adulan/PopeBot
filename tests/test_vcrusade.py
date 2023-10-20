import unittest, os
from unittest.mock import Mock, patch
import src.exceptions as exceptions
from math import log

class CrusadeTests(unittest.IsolatedAsyncioTestCase):
    test_crusade = None

    @patch('os.getenv')
    def setUp(self, mock_genenv):
        #Suppress print statements
        import sys
        sys.stdout = open(os.devnull, 'w')

        #Suppress warnings
        import warnings
        warnings.filterwarnings("ignore")
        
        sys.modules['constants'] = __import__('src.constants')
        sys.modules['constants'].GUILD_ID = 1234567890
        sys.modules['cardinal'] = __import__('src.cardinal')
       
        #sys.modules['utils'] = __import__('src.utils')
        import src.utils as utils
        sys.modules['utils'] = utils
        
        from src import crusade
        sys.modules['crusade'] = crusade
        global test_crusade
        test_crusade = crusade.Crusade(Mock(), "Test Name", "City1", "City2")      

    def test_add_attacking_soldier_not_cardinal(self):
        cardinal = Mock()
        cardinal.member = Mock()
        global test_crusade
        
        with patch("src.crusade.get_member_from_cardinal_list", return_value=None):
            self.assertRaises(exceptions.MemberNotCardinal, test_crusade.add_attacking_soldier, cardinal)


    def test_add_defending_soldier(self):
        cardinal = Mock()
        member = Mock()
        cardinal.id = 1234
        member.id = 1234
        cardinal.member = member
        global test_crusade
        
        with patch("src.utils.cardinal_list", [cardinal]):
            test_crusade.add_defending_soldier(cardinal)
        assert test_crusade.defending_army == [cardinal]
        assert test_crusade.defending_general == cardinal


    def test_add_attacking_funding_new_soldier(self):
        cardinal = Mock()
        member = Mock()
        cardinal.id = 1234
        cardinal.pope_points = 1000
        member.id = 1234
        cardinal.member = member
        global test_crusade
        mock_add_attacking_soldier = Mock()
        
        with patch("src.utils.cardinal_list", [cardinal]), patch("src.crusade.Crusade.add_attacking_soldier", mock_add_attacking_soldier):
            test_crusade._add_attacking_funding(cardinal, 100, 100)
        mock_add_attacking_soldier.assert_called_once_with(cardinal) == None
        assert test_crusade.attacking_funding == 100
        assert cardinal.pope_points == 900


    def test_add_defending_funding(self):
        cardinal = Mock()
        member = Mock()
        cardinal.id = 1234
        cardinal.pope_points = 1000
        member.id = 1234
        cardinal.member = member
        global test_crusade
        test_crusade.defending_army = [cardinal]
        mock_add_defending_soldier = Mock()
        
        with patch("src.utils.cardinal_list", [cardinal]), patch("src.crusade.Crusade.add_defending_soldier", mock_add_defending_soldier):
            test_crusade._add_defending_funding(cardinal, 100, 100)
        mock_add_defending_soldier.assert_not_called() == None
        assert test_crusade.defending_funding == 100
        cardinal.add_pope_points.assert_called_once_with(-100) == None


    def test_add_defending_funding_new_soldier(self):
        cardinal = Mock()
        member = Mock()
        cardinal.id = 1234
        cardinal.pope_points = 1000
        member.id = 1234
        cardinal.member = member
        global test_crusade
        mock_add_defending_soldier = Mock()
        
        with patch("src.utils.cardinal_list", [cardinal]), patch("src.crusade.Crusade.add_defending_soldier", mock_add_defending_soldier):
            test_crusade._add_defending_funding(cardinal, 100, 100)
        mock_add_defending_soldier.assert_called_once_with(cardinal) == None
        assert test_crusade.defending_funding == 100
        cardinal.add_pope_points.assert_called_once_with(-100) == None


    def test_attacking_army_strength(self):
        cardinal1 = Mock()
        member1 = Mock()
        cardinal1.id = 1234
        cardinal1.popeliness.return_value = 1000
        cardinal1.sin_coins = 25
        member1.id = 1234
        cardinal1.member = member1
        cardinal2 = Mock()
        member2 = Mock()
        cardinal2.id = 12345
        cardinal2.popeliness.return_value = 1000
        cardinal2.sin_coins = 100
        member2.id = 12345
        cardinal2.member = member2
        global test_crusade
        test_crusade.attacking_army = [cardinal1, cardinal2]
        test_crusade.attacking_funding = 500
        # first log value = (1000-25) + (1000-100) + (500/2)
        self.assertEqual(test_crusade.attacking_army_strength(), log(2125, 2))


    def test_attacking_army_strength_no_army(self):
        global test_crusade
        test_crusade.attacking_army = []
        test_crusade.attacking_funding = 500
        
        self.assertEqual(test_crusade.attacking_army_strength(), 0)


    def test_attacking_army_strength_army_zero(self):
        cardinal1 = Mock()
        member1 = Mock()
        cardinal1.id = 1234
        cardinal1.popeliness.return_value = 0
        cardinal1.sin_coins = 0
        member1.id = 1234
        cardinal1.member = member1
       
        global test_crusade
        test_crusade.attacking_army = [cardinal1]
        test_crusade.attacking_funding = 0

        self.assertEqual(test_crusade.attacking_army_strength(), 0)


    def test_defending_army_strength(self):
        cardinal1 = Mock()
        member1 = Mock()
        cardinal1.id = 1234
        cardinal1.popeliness.return_value = 1000
        cardinal1.sin_coins = 25
        member1.id = 1234
        cardinal1.member = member1
        cardinal2 = Mock()
        member2 = Mock()
        cardinal2.id = 12345
        cardinal2.popeliness.return_value = 1000
        cardinal2.sin_coins = 100
        member2.id = 12345
        cardinal2.member = member2
        global test_crusade
        test_crusade.defending_army = [cardinal1, cardinal2]
        test_crusade.defending_funding = 500
        # first log value = (1000-25) + (1000-100) + (500/2)
        self.assertEqual(test_crusade.defending_army_strength(), log(2125, 2))


    def test_defending_army_strength_no_army(self):
        global test_crusade
        test_crusade.defending_army = []
        test_crusade.defending_funding = 500
        
        self.assertEqual(test_crusade.defending_army_strength(), 0)


    def test_defending_army_strength_army_zero(self):
        cardinal1 = Mock()
        member1 = Mock()
        cardinal1.id = 1234
        cardinal1.popeliness.return_value = 0
        cardinal1.sin_coins = 0
        member1.id = 1234
        cardinal1.member = member1
       
        global test_crusade
        test_crusade.defending_army = [cardinal1]
        test_crusade.defending_funding = 0

        self.assertEqual(test_crusade.defending_army_strength(), 0)


    async def test_conclude_crusade_attack_win(self):
        from src.cardinal import Cardinal
        
        member1 = Mock()
        member1.id = 1234
        cardinal1 = Cardinal(member1)
        cardinal1.id = 1234
        cardinal1.sin_coins = 25
        cardinal1.pope_points = 1000
        
        cardinal1.member = member1
        
        member2 = Mock()
        member2.id = 12345
        cardinal2 = Cardinal(member2)
        cardinal2.id = 12345
        cardinal2.sin_coins = 100
        cardinal2.pope_points = 1000
        
        cardinal2.member = member2
        
        member3 = Mock()
        member3.id = 123456
        cardinal3 = Cardinal(member3)
        cardinal3.id = 123456
        cardinal3.sin_coins = 100
        cardinal3.pope_points = 1000
        
        global test_crusade
        test_crusade.attacking_army = [cardinal1, cardinal2]
        test_crusade.attacking_funding = 5000
        test_crusade.defending_army = [cardinal3]
        test_crusade.defending_funding = 1000
        test_crusade.attacking_general = cardinal1
        test_crusade.defending_general = cardinal3
        
        await test_crusade.conclude_crusade()
        self.assertEqual(cardinal1.pope_points, 5000)
        self.assertEqual(cardinal2.pope_points, 4000)
        self.assertEqual(cardinal3.pope_points, 1000)
        self.assertEqual(cardinal3.sin_coins, 0)
        self.assertEqual(test_crusade.attacking_funding, 0)
        self.assertEqual(test_crusade.defending_funding, 0)
        self.assertEqual(test_crusade.attacking_army, [])
        self.assertEqual(test_crusade.defending_army, [])
        self.assertEqual(test_crusade.attacking_general, None)
        self.assertEqual(test_crusade.defending_general, None)
            
    
    async def test_conclude_crusade_defend_win(self):
        from src.cardinal import Cardinal
        
        member1 = Mock()
        member1.id = 1234
        cardinal1 = Cardinal(member1)
        cardinal1.id = 1234
        cardinal1.sin_coins = 25
        cardinal1.pope_points = 1000
        
        cardinal1.member = member1
        
        member2 = Mock()
        member2.id = 12345
        cardinal2 = Cardinal(member2)
        cardinal2.id = 12345
        cardinal2.sin_coins = 100
        cardinal2.pope_points = 1000
        
        cardinal2.member = member2
        
        member3 = Mock()
        member3.id = 123456
        cardinal3 = Cardinal(member3)
        cardinal3.id = 123456
        cardinal3.sin_coins = 100
        cardinal3.pope_points = 1000
        
        global test_crusade
        test_crusade.attacking_army = [cardinal3]
        test_crusade.attacking_funding = 1000
        test_crusade.defending_army = [cardinal1, cardinal2]
        test_crusade.defending_funding = 5000
        test_crusade.attacking_general = cardinal3
        test_crusade.defending_general = cardinal1
        
        await test_crusade.conclude_crusade()
        self.assertEqual(cardinal1.pope_points, 5000)
        self.assertEqual(cardinal2.pope_points, 4000)
        self.assertEqual(cardinal3.pope_points, 1000)
        self.assertEqual(cardinal3.sin_coins, 1100)
        self.assertEqual(test_crusade.attacking_funding, 0)
        self.assertEqual(test_crusade.defending_funding, 0)
        self.assertEqual(test_crusade.attacking_army, [])
        self.assertEqual(test_crusade.defending_army, [])
        self.assertEqual(test_crusade.attacking_general, None)
        self.assertEqual(test_crusade.defending_general, None)


if __name__ == '__main__':
    unittest.main()