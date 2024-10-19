import unittest
from adventure_game import Room, Item, Player, NPC, save_game, load_game
import io
from contextlib import redirect_stdout

class TestAdventureGame(unittest.TestCase):
    def setUp(self):
        # Set up a simple game environment
        self.room = Room("Test Room", "This is a test room.")
        self.item = Item("Test Item", "This is a test item.")
        self.room.add_item(self.item)
        self.player = Player(self.room)
    
    def test_pick_up_item(self):
        self.player.pick_up("Test Item")
        self.assertIn(self.item, self.player.inventory)
        self.assertNotIn(self.item, self.room.items)
    
    def test_move_invalid_direction(self):
        f = io.StringIO()
        with redirect_stdout(f):
            self.player.move("sideways")  # Invalid direction
        output = f.getvalue()
        self.assertIn("Invalid direction.", output)
    
    def test_move_unavailable_direction(self):
        f = io.StringIO()
        with redirect_stdout(f):
            self.player.move("up")  # Valid direction, no exit
        output = f.getvalue()
        self.assertIn("You can't go that way.", output)
    
    def test_talk_to_npc(self):
        npc = NPC("Test NPC", "Hello!")
        self.room.add_npc(npc)
        f = io.StringIO()
        with redirect_stdout(f):
            self.player.talk_to("Test NPC")
        output = f.getvalue()
        self.assertIn("Test NPC says: 'Hello!'", output)
    
    def test_save_and_load_game(self):
        self.player.pick_up("Test Item")
        save_game(self.player)
        new_player = load_game()
        self.assertEqual(new_player.inventory[0].name, "Test Item")

if __name__ == '__main__':
    unittest.main()
