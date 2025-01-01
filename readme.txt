15-112 Term Project by Graham Felton (gtf): "Dungeon Craw112r"
                                                                               _____
  ____________ ______   _____    _____    _____            _____          _____\    \       ____    _____    _____
  \           \\     \  \    \  |\    \   \    \      _____\    \_       /    / |    |  ____\_  \__|\    \   \    \
   \           \\    |  |    |   \\    \   |    |    /     /|     |     /    /  /___/| /     /     \\\    \   |    |
    |    /\     ||   |  |    |    \\    \  |    |   /     / /____/|    |    |__ |___|//     /\      |\\    \  |    |
    |   |  |    ||    \_/   /|     \|    \ |    |  |     | |_____|/    |       \     |     |  |     | \|    \ |    |
    |    \/     ||\         \|      |     \|    |  |     | |_________  |     __/ __  |     |  |     |  |     \|    |
   /           /|| \         \__   /     /\      \ |\     \|\        \ |\    \  /  \ |     | /     /| /     /\      \
  /___________/ | \ \_____/\    \ /_____/ /______/|| \_____\|    |\__/|| \____\/    ||\     \_____/ |/_____/ /______/|
 |           | /   \ |    |/___/||      | |     | || |     /____/| | ||| |    |____/|| \_____\   | /|      | |     | |
 |___________|/     \|____|   | ||______|/|_____|/  \|_____|     |\|_|/ \|____|   | | \ |    |___|/ |______|/|_____|/
                          |___|/                           |____/             |___|/   \|____|     _____
         _____  ___________          _____           _______     _______  _____               _____\    \ ___________
    _____\    \_\          \       /      |_        /      /|   |\      \|\    \             /    / |    |\          \
   /     /|     |\    /\    \     /         \      /      / |   | \      \\\    \           /    /  /___/| \    /\    \
  /     / /____/| |   \_\    |   |     /\    \    |      /  |___|  \      |\\    \         |    |__ |___|/  |   \_\    |
 |     | |____|/  |      ___/    |    |  |    \   |      |  |   |  |      | \|    | ______ |       \        |      ___/
 |     |  _____   |      \  ____ |     \/      \  |       \ \   / /       |  |    |/      \|     __/ __     |      \  ____
 |\     \|\    \ /     /\ \/    \|\      /\     \ |      |\\/   \//|      |  /            ||\    \  /  \   /     /\ \/    \
 | \_____\|    |/_____/ |\______|| \_____\ \_____\|\_____\|\_____/|/_____/| /_____/\_____/|| \____\/    | /_____/ |\______|
 | |     /____/||     | | |     || |     | |     || |     | |   | |     | ||      | |    ||| |    |____/| |     | | |     |
  \|_____|    |||_____|/ \|_____| \|_____|\|_____| \|_____|\|___|/|_____|/ |______|/|____|/ \|____|   | | |_____|/ \|_____|
         |____|/                                                                                  |___|/

WHAT IS IT?

Dungeon Craw112r is dungeon crawler-lite game using raycasting to create a 3d representation of a 2D game board.
The player is encouraged to explore the level in order to find items but watch out for enemies! There are two
enemies per level which are constantly chasing the player. When within a close enough distance, a combat state
is triggered and the player must fight to defend themselves. Combat is turn based, meaning the player can choose
from 4 hitboxes (head, chest, left arm, right arm) with each having a certain chance to hit the enemy and do
damage. The enemy then takes their turn, attempting to hit the player for 10 damage with a 40% chance to hit.
When the player defeats the enemy, the game state returns to the level and the player can access their inventory
to heal any health they lost. If the player is defeated, they are greeted with a 'Game Over' screen, where they
can press 'r' to return to the main menu and start a new game. If the player survives all 4 levels and makes it 
to the final door, they win the game.


TO RUN:

1. open draw.py in your favorite python editor
2. press 'run'
3. enjoy!

no external modules used outside of cmu_graphics

ascii art from http://patorjk.com/