import unittest, os
from unittest.mock import Mock
from src import cardinal


class CardinalTests(unittest.TestCase):
    
    def setUp(self):
        #Suppress print statements
        import sys
        sys.stdout = open(os.devnull, 'w')
        
        #Suppress warnings
        import warnings
        warnings.filterwarnings("ignore")


    # Test Cardinal Initialization
    def test_cardinal_init(self):
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        test_cardinal = cardinal.Cardinal(member)
        assert test_cardinal.member == member
        assert test_cardinal.name == "Test Cardinal"
        assert test_cardinal.id == 1234567890
        assert test_cardinal.pope_points == 0
        assert test_cardinal.sin_coins == 0


    # Test Cardinal add_pope_points
    def test_cardinal_add_pope_points(self):
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        test_cardinal = cardinal.Cardinal(member)
        test_cardinal.add_pope_points(10)
        assert test_cardinal.pope_points == 10
        test_cardinal.add_pope_points(5)
        assert test_cardinal.pope_points == 15


    # Test Cardinal add_sin_coins
    def test_cardinal_add_sin_coins(self):
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        test_cardinal = cardinal.Cardinal(member)
        test_cardinal.add_sin_coins(10)
        assert test_cardinal.sin_coins == 10
        test_cardinal.add_sin_coins(5)
        assert test_cardinal.sin_coins == 15


    # Test Cardinal popeliness
    def test_cardinal_popeliness(self):
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        test_cardinal = cardinal.Cardinal(member)
        
        test_cardinal.add_pope_points(10)
        test_cardinal.add_sin_coins(5)
        assert test_cardinal.popeliness() == 0
        
        test_cardinal.add_pope_points(5)
        test_cardinal.add_sin_coins(10)
        assert test_cardinal.popeliness() == -15
       
        test_cardinal.add_pope_points(10)
        test_cardinal.add_sin_coins(5)
        assert test_cardinal.popeliness() == -15
        
        test_cardinal.add_pope_points(5)
        test_cardinal.add_sin_coins(10)
        assert test_cardinal.popeliness() == -30


    # Test Cardinal to_json
    def test_cardinal_to_json(self):
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        test_cardinal = cardinal.Cardinal(member)
        test_cardinal.add_pope_points(10)
        test_cardinal.add_sin_coins(5)
        assert test_cardinal.to_json() == {
            "name": "Test Cardinal",
            "id": 1234567890,
            "pope_points": 10,
            "sin_coins": 5
        }

    
    # Test Cardinal from_json
    def test_cardinal_from_json(self):
        member = Mock()
        member.name = "Test Cardinal"
        member.id = 1234567890
        
        test_cardinal = cardinal.Cardinal(member)
        test_cardinal.from_json({
            "name": "Test Cardinal",
            "id": 1234567890,
            "pope_points": 10,
            "sin_coins": 5
        })

        assert test_cardinal.name == "Test Cardinal"
        assert test_cardinal.id == 1234567890
        assert test_cardinal.pope_points == 10
        assert test_cardinal.sin_coins == 5


if __name__ == '__main__':
    unittest.main()