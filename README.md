# PyQT5 Snake Game
Made by Мельников Сергей, Гарипов Назар (оба КН-201)

# Gameplay
In general, its almost classic snake game, but with multiple levels (maps) and portals.

Travel across the map and eat food (red cell) to grow your snake.
Food always remains as one point, which is respawned randomly at empty point as you eat existent one.

Any snake head collision with either its tail, either obstacle (dark blue cell) leads to death and, therefore, game over.
No spare lives provided - keep that in mind.
  

Some levels contain portals (light blue cell), which would teleport snake somewhere once snake's head moved through it.
Some portals teleport snake to a random empty point, some - to a static one, depending on portal type.
Static portal destination points are marked as orange cells and are not obstacles, but doesn't work as teleport to portal origin point - portals are single-directed.
Random portals chooses its teleportation destination that way, which guarantees you to have at least one empty cell on your way, assuming you didn't change snake direction during teleportation. 

After a certain amount of food eaten at the level a transition portal (also light blue cell) would appear at a random empty point.
It would teleport your snake to the next level.

After you leave the last level this game has, it is considered you've won and the game is over.

# Controls
* Use keyboard arrows to change snake direction
* Spam any button to speed up snake


# Dependencies
* PyQT 5 for GUI
* PyTest (optional for tests)

You can install it via `pip install -r requirements.txt`
    
# Tests coverage 
 * game.py - 91%    // game model class
 * snake.py - 100%  // snake auxiliary class for game model

# Custom levels
It is possible to create your own levels for this game.

Game level consists of game map, initial snake instance, and level clear score.
Level clear score is an amount of eat that must be eaten at this level before a transition portal would appear.
Game map must be generated according to width and height provided.
Initial snake instance is used if this level is first in the list.
Otherwise, existent snake is being teleported to level's initial snake's head position.
Snake is defined as its head and tail point, by the way.

Once a new level is created, it can be imported, instanced and placed at levels order list at main.py

See abstract classes GameLevel, GameMap and Portal class too at common/level.py and common/game_map.py for further details.
It is quite trivial to write your level using existent levels as an example if you're accustomed to python code and able to read other's code.
Unfortunately, I have no time to describe a process with more details, but I must state, that such extension point is present.
