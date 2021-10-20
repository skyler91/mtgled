import unittest
from gamecontroller import GameController, NUM_LIGHTS
from unittest.mock import MagicMock, patch

TEST_PLAYERS = [
            {
                'name': 'Player 1',
                'number': 1,
                'color': '#ff0000',
                'lightStart': 0,
                'lightEnd': 25
            },
            {
                'name': 'Player 2',
                'number': 2,
                'color': '#00ff00',
                'lightStart': 25,
                'lightEnd': 50
            },
            {
                'name': 'Player 6',
                'number': 6,
                'color': '#0000ff',
                'lightStart': 124,
                'lightEnd': 148
            }
        ]

class TestGameController(unittest.TestCase):
    def setUp(self):
        self.context = MagicMock()
        self.gc = GameController(self.context)

    def tearDown(self):
        self.gc.shutdown()

    def test_init_lights(self):
        self.assertEqual(self.gc.init_lights(), [{'r': 0, 'g': 0, 'b': 0}] * NUM_LIGHTS)

    def test_init_lights_green(self):
        self.assertEqual(self.gc.init_lights((0,255,0)), [{'r': 0, 'g': 255, 'b': 0}] * NUM_LIGHTS)

    @patch('time.sleep')
    def test_new_game(self, mock):
        self.gc.new_game(TEST_PLAYERS)
        self.assertEqual(3, len(self.gc.players))
        self.assertTrue(self.gc.game_in_progress)
        self.assertEqual(1, self.gc.current_player.number)
        # player 1 is red
        self.check_lights(list(range(25)), (255, 0, 0))
        # all other lights off
        self.check_lights(list(range(25, NUM_LIGHTS)), (0,0,0))

    @patch('time.sleep')
    def test_turn_cycle(self, mock):
        self.gc.new_game(TEST_PLAYERS)
        self.assertTrue(self.gc.game_in_progress)
        self.assertEqual(1, self.gc.current_player.number)

        # go to player 2's turn
        self.gc.next_turn()
        self.assertEqual(2, self.gc.current_player.number)
        # player 2 is green
        self.check_lights(list(range(25,50)), (0,255,0))
        # all other lights off
        self.check_lights(list(range(25)) + list(range(50, NUM_LIGHTS)), (0,0,0))

        # go to player 6's turn
        self.gc.next_turn()
        self.assertEqual(6, self.gc.current_player.number)
        # player 6 is blue
        self.check_lights(list(range(124, NUM_LIGHTS)), (0,0,255))
        # all other lights off
        self.check_lights(list(range(124)), (0,0,0))

        # back to player 1
        self.gc.next_turn()
        self.assertEqual(1, self.gc.current_player.number)
        # player 1 is red
        self.check_lights(list(range(25)), (255, 0, 0))
        # all other lights off
        self.check_lights(list(range(25, NUM_LIGHTS)), (0,0,0))

    @patch('time.sleep')
    def test_reset_game(self, mock):
        self.gc.new_game(TEST_PLAYERS)
        self.gc.reset_game()
        self.assertFalse(self.gc.game_in_progress)
        self.assertEqual(0, self.gc.current_player)
        self.assertEqual([], self.gc.players)
        # all lights off
        self.check_lights(list(range(NUM_LIGHTS)), (0,0,0))

    def test_update_all_lights(self):
        # set lights to white
        self.gc.update_all_lights((255,255,255))
        self.check_lights(list(range(NUM_LIGHTS)), (255,255,255))

    def test_update_lights(self):
        self.gc.update_lights(list(range(5,20)), (255,0,0))
        self.check_lights(list(range(5,20)), (255,0,0))
        self.check_lights(list(range(5)) + list(range(20, NUM_LIGHTS)), (0,0,0))

        self.gc.update_lights(list(range(15,30)), (0,255,0))
        self.check_lights(list(range(5,15)), (255,0,0))
        self.check_lights(list(range(15,30)), (0,255,0))
        self.check_lights(list(range(5)) + list(range(30, NUM_LIGHTS)), (0,0,0))

    def test_lights_off(self):
        self.gc.update_all_lights((255,0,0))
        self.gc.lights_off()
        self.check_lights(list(range(NUM_LIGHTS)), (0,0,0))

    def check_lights(self, light_indices, color):
        for light_index in light_indices:
            self.assertEqual({'r': color[0], 'g': color[1], 'b': color[2]}, self.gc.lights[light_index])
