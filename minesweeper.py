import math
import random


# -------------------------------------------------------------------
#
#  Basic Information
#
# -------------------------------------------------------------------
x = 0
y = 0


# Asks for the Height and Width Value of the Minesweeper
while (x <= 0): 
    x = input("Width: ")
    try:
        x = int(x)
    except ValueError:
        x = -10000

while (y <= 0): 
    y = input("Height: ")
    try:
        y = int(y)
    except ValueError:
        y = -10000




global landminepercentage
landminepercentage = 0.0
while (landminepercentage >= 1) or (landminepercentage <= 0): 
    landminepercentage = input("Landmine Percentage (Enter value, where 0<value<1): ")
    try:
        landminepercentage = float(landminepercentage)
    except ValueError:
        landminepercentage = 0.0





# Calculate the number of landmines required to spawn.
landminecount = math.floor(landminepercentage * x*y)
# Adds a map
map = []






click_x = 0
click_y = 0

# -------------------------------------------------------------------
# 
#  Map Generation
#
# -------------------------------------------------------------------


def map_generation():
    # -------------------------------------------------------------------
    # 
    #  Map Generation (Put down landmines)
    #
    # -------------------------------------------------------------------

    # Generates a map for the Minesweeper
    for i in range(0, x*y - landminecount):
        map.insert(0,0)
        
    for i in range(0, landminecount):
        map.insert(0,"L")

    # Randomizes the landmine map
    random.shuffle(map)


    # -------------------------------------------------------------------
    # 
    #  Map Generation (Add Numbers to the map)
    #
    # -------------------------------------------------------------------
    for i in range(0,x*y):
        if map[i] == "L":
            # Add 1 to each of the grids on the left and the right of the landmine
            # However, it detects whether the landmines are on the same line
            if (math.floor((i+1)/x) == math.floor(i/x)) and map[i+1] != "L":
                map[i+1] += 1
            if (math.floor((i-1)/x) == math.floor(i/x)) and map[i-1] != "L":
                map[i-1] += 1


            # Adds 1 to each of the grids above and below the landmine
            # We can't combine the two if statements as the latter one may cause errors
            if math.floor((i+x)/x) < y:
                if (math.floor((i+x)/x) == math.floor(i/x) + 1) and map[i+x] != "L":
                    map[i+x] += 1
            if math.floor((i-x)/x) >= 0:
                if (math.floor((i-x)/x) == math.floor(i/x) - 1) and map[i-x] != "L":
                    map[i-x] += 1


            # Adds 1 to each of the grids the four corners of the landmine
            # We can't combine the two if statements as the latter one may cause errors
            if math.floor((i+x +1)/x) < y:
                if (math.floor((i+x +1)/x) == math.floor(i/x) + 1) and map[i+x+1] != "L":
                    map[i+x +1] += 1
            if math.floor((i+x -1)/x) < y:
                if (math.floor((i+x -1)/x) == math.floor(i/x) + 1) and map[i+x-1] != "L":
                    map[i+x -1] += 1

            if math.floor((i-x +1)/x) >= 0:
                if (math.floor((i-x +1)/x) == math.floor(i/x) - 1) and map[i-x+1] != "L":
                    map[i-x +1] += 1
            if math.floor((i-x -1)/x) >= 0:
                if (math.floor((i-x -1)/x) == math.floor(i/x) - 1) and map[i-x-1] != "L":
                    map[i-x -1] += 1

map_generation()

# -------------------------------------------------------------------
# 
#  Declare a UI
# 
# -------------------------------------------------------------------

# Adds a UI
UI = []

# declare UI
for n in range(0, y):
    UI.insert(0,[])
    for m in range(0, x):
        UI[0].insert(0,'⬛')


# -------------------------------------------------------------------
# 
#  Add a function to render the landmine map (Basically rendering the fancy map)
# 
# -------------------------------------------------------------------
def render():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nSelected: \nX: ", click_x, "  Y: ", click_y)
    list_of_x = []
    for i in range(0,x):
        if i<10:
            list_of_x.append("0" + str(i)) 
        else:
            list_of_x.append(str(i)) 
    print("  ", *list_of_x, "[X]", sep=" ")
    for n in range(0,y):
        if n<10:
            print("0" + str(n), *UI[n], sep=" ")
        else:
            print(n, *UI[n], sep=" ")
    print("[Y]\n")



# -------------------------------------------------------------------
# 
#  Game
# 
# -------------------------------------------------------------------

# This is a bool for ended or not ended (0: not ended, 1: ended)
ended = 0
# This is a bool for first_turn or not first_turn (0: not first_turn, 1: first_turn)
global first_turn
first_turn = 1

tiles_left = x*y
    

def move(location_x,location_y,currentmap):
    global tiles_left
    global ended
    global map


    # Keeps count of the number of tiles left, to detect whether it is the same with the number of landmines. If it is, then the game has ended.
    tiles_left -= 1
    location = location_y * x + location_x

    # Saves currentmap[location] into a temp variable, for easier access
    temp = currentmap[location]
    
    
    # Detects whether the selected block is a landmine, if it is, it gets subdivided to 2 branches.
    ####### 1. If it is the player's first move, (aka "first_turn == 1"), then the map gets refreshed until that block is not a landmine, then continue running the scriptpygame.examples.mask.main()
    ####### 2. If it is NOT the player's first move, (aka "first_turn == 0"), then the game announces that the player has lost.
    if temp == "L":
        # 1. Player's first move
        if first_turn == 1:
            while temp == "L":
                print("reloading")
                map = []
                map_generation()
                temp = map[location]
        # 2. Player Lost
        else: 
            UI[location_y][location_x] = "💣"
            ended = 1
            # Show bomb locations:
            for i in range(0,x):
                for j in range(0,y):
                    if map[i * x + j] == "L":
                        UI[i][j] = "💣"
            render()
            print("\n\nYou Lost :(")
    
    # Detects whether the selected block is an unrevealed block.
    ####### Note:
    ####### 
    ####### This code first detects whether it's an unrevealed block,
    ####### then starts to detect if the 8 surrounding blocks are unrevealed blocks as well, then convert them into revealed ones
    ####### which works by **function threading**.
    #######
    #######
    if temp == 0:
        UI[location_y][location_x] = "⬜"

        ### Open up nearby holes
        # Reveals the grids on the left and the right of the landmine
        # However, it detects whether the landmines are on the same line
        if (math.floor((location+1)/x) == math.floor(location/x)) and UI[location_y][location_x+1] == '⬛':
            move(location_x+1,location_y,currentmap)
        if (math.floor((location-1)/x) == math.floor(location/x)) and UI[location_y][location_x-1] == '⬛':
            move(location_x-1,location_y,currentmap)


        # Reveals the grids above and below the landmine
        # We can't combine the two if statements as the latter one may cause errors
        if math.floor((location+x)/x) < y:
            if (math.floor((location+x)/x) == math.floor(location/x) + 1) and UI[location_y+1][location_x] == '⬛':
                move(location_x,location_y+1,currentmap)
        if math.floor((location-x)/x) >= 0:
            if (math.floor((location-x)/x) == math.floor(location/x) - 1) and UI[location_y-1][location_x] == '⬛':
                move(location_x,location_y-1,currentmap)


        # Reveals the grids at the four corners of the landmine
        # We can't combine the two if statements as the latter one may cause errors
        if math.floor((location+x +1)/x) < y:
            if (math.floor((location+x +1)/x) == math.floor(location/x) + 1) and UI[location_y+1][location_x+1] == '⬛':
                move(location_x+1,location_y+1,currentmap)
        if math.floor((location+x -1)/x) < y:
            if (math.floor((location+x -1)/x) == math.floor(location/x) + 1) and UI[location_y+1][location_x-1] == '⬛':
                move(location_x-1,location_y+1,currentmap)

        if math.floor((location-x +1)/x) >= 0:
            if (math.floor((location-x +1)/x) == math.floor(location/x) - 1) and UI[location_y-1][location_x+1] == '⬛':
                move(location_x+1,location_y-1,currentmap)
        if math.floor((location-x -1)/x) >= 0:
            if (math.floor((location-x -1)/x) == math.floor(location/x) - 1) and UI[location_y-1][location_x-1] == '⬛':
                move(location_x-1,location_y-1,currentmap)


    
    elif temp == "L":
        return
    else:
        UI[location_y][location_x] = " " + str(temp)




# -------------------------------------------------------------------
# 
#  Start Game
# 
# -------------------------------------------------------------------

global mode
mode = -1


# At first, it renders the map
while ended==0:
    print(map)
    # While the game hasn't ended, the code will continue to ask for what move you want to choose
    render()

    # Reset mode, click_x and click_y
    click_x = -1
    click_y = -1
    mode = -1


    # Setting up a while loop to constantly ask the player for info if they typed info which would result in errors.
    while not (mode == -31415 or (int(mode) >= 0 and int(mode) < x)): 
        mode = input("(Type \"Flag\" if you want to flag a block.)\n\nX Coord:  ")
        # Represent Flag mode with a negative number (Negative number because it can't be chosen)
        if mode == "Flag":
            mode = -31415

        # Here, the code tries to convert mode (which is the player input) into an integer. If it fails, then the code sets the "mode" variable to -10000, which then fulfills the while loop, and asks the player info again.
        try:
            mode = int(mode)
        except ValueError:
            mode = -10000

    # Detects whether Flag mode have been chosen.
    if mode == -31415:
        # Setting up a while loop to constantly ask the player for info if they typed info which would result in errors.
        click_x = -1
        while not (click_x >= 0 and click_x < x): 
            click_x = input("[Flag] X Coord: ")

            # Here, the code tries to convert mode (which is the player input) into an integer. If it fails, then the code sets the "mode" variable to -10000, which then fulfills the while loop, and asks the player info again.
            try:
                click_x = int(click_x)
            except ValueError:
                click_x = -10000

        # Setting up a while loop to constantly ask the player for info if they typed info which would result in errors.
        click_y = "N/A"
        render()
        click_y = -1
        while not (click_y >= 0 and click_y < y): 
            click_y = input("[Flag] Y Coord: ")

            # Here, the code tries to convert mode (which is the player input) into an integer. If it fails, then the code sets the "mode" variable to -10000, which then fulfills the while loop, and asks the player info again.
            try:
                click_y = int(click_y)
            except ValueError:
                click_y = -10000


        # Flagging the block selected by the player
        if UI[click_y][click_x] == "🟥":
            UI[click_y][click_x] =  "⬛"
        elif UI[click_y][click_x] == "⬛":
            UI[click_y][click_x] = "🟥"

    # Regular choose block mode
    else:
        # This line converts "mode" over to int, then throwing it into the "click_x" var
        click_x = int(mode)
        click_y = "N/A"
        render()

        # Setting up a while loop to constantly ask the player for info if they typed info which would result in errors.
        click_y = -1
        while not (click_y >= 0 and click_y < y): 
            click_y = input("Y Coord: ")
            # Here, the code tries to convert mode (which is the player input) into an integer. If it fails, then the code sets the "mode" variable to -10000, which then fulfills the while loop, and asks the player info again.
            try:
                click_y = int(click_y)
            except ValueError:
                click_y = -10000
        # Apply the move with the "move()" function
        move(click_x,click_y,map)
        # Sets the boolean "first_turn" to false, so that move() won't automatically refresh the map if the player's first move is a landmine.
        first_turn = 0

    # Checks if the player has won
    if landminecount == tiles_left:
        render()
        print("\n\nYou Won!")
        ended = 1