# Krish Patel and Jeremy Chong
# 4/28/2024
# Main
# This is the main function, the start of the game will be ran through here

#importing packages
import climage
import random
import os
from boxing import boxing

#Colour variables
GREEN = '\033[1;32m'
RESET = '\033[0m'
BOLD = '\033[1m'
CYAN = '\033[96m'
RED = '\033[31m'
YELLOW = '\u001b[33m'
LIME = '\u001b[38;2;81;224;141m'
LBLUE = '\u001b[38;2;27;224;242m'
PURPLE = '\u001b[38;2;59;21;212m'
GREEN_BACK = '\x1b[6;30;42m'

#Game variables
userGrid = [
  [8, 0, 0, 0, 0, 0, 0, 0, 0],
  [6, 0, 0, 0, 0, 0, 0, 0, 0],
  [7, 0, 0, 0, 0, 0, 0, 0, 0],
  [5, 0, 0, 0, 0, 0, 0, 0, 0],
  [4, 0, 0, 0, 0, 0, 0, 0, 0],
  [3, 0, 0, 0, 0, 0, 0, 0, 0],
  [2, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0],
  [" ", 1, 2, 3, 4, 5, 6, 7, 8]
]

oppGrid = [
  [8, 0, 0, 0, 0, 0, 0, 0, 0],
  [7, 0, 0, 0, 0, 0, 0, 0, 0],
  [6, 0, 0, 0, 0, 0, 0, 0, 0],
  [5, 0, 0, 0, 0, 0, 0, 0, 0],
  [4, 0, 0, 0, 0, 0, 0, 0, 0],
  [3, 0, 0, 0, 0, 0, 0, 0, 0],
  [2, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0],
  [" ", 1, 2, 3, 4, 5, 6, 7, 8]
]

oppGridDisplay = [
  [8, 0, 0, 0, 0, 0, 0, 0, 0],
  [7, 0, 0, 0, 0, 0, 0, 0, 0],
  [6, 0, 0, 0, 0, 0, 0, 0, 0],
  [5, 0, 0, 0, 0, 0, 0, 0, 0],
  [4, 0, 0, 0, 0, 0, 0, 0, 0],
  [3, 0, 0, 0, 0, 0, 0, 0, 0],
  [2, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0],
  [" ", 1, 2, 3, 4, 5, 6, 7, 8]
]

# The 4 ships are: Battleship (4), Cruiser (3), Submarine (3), and Destroyer (2)
ships = [4, 3, 3, 2]
shipSymbols = ["⛴️", "🚤", "⛵", "🚢"]

userMiss = 0
oppMiss = 0

userActiveShips = ["⛴️", "🚤", "⛵", "🚢"]
oppActiveShips = ["⛴️", "🚤", "⛵", "🚢"]

shipNames = ["battleship", "cruiser", "submarine", "destroyer"]

possibleHits = []

#Variables that control the game system
quit = False
gameFinished = False

# This function clears the console
def clearConsole():
  os.system('clear')

# Get valid x and y coordinates from the user
def getCoordinates(location, boat):
  getX = True
  getY = False
  while True:
    try:
      while getX: # getting a valid x coordinate
        if location == "P":
          posX = int(input("Enter the x-position where you want to place the " + boat + ": "))
        elif location == "D":
          posX = int(input("Enter the x-position where you want to hit: "))
        if posX < 1 or posX > 8:
          print(RED + BOLD + "Enter a number between 1 and 8 (inclusive)!" + RESET)
        else:
          getX = False
          getY = True
          break
          
      while getY: # getting a valid y coordinate
        if location == "P":
          posY = int(input("Enter the y-position where you want to place the " + boat + ": "))
        elif location == "D":
          posY = int(input("Enter the y-position where you want to hit: "))
        if posY < 1 or posY > 8:
          print(RED + BOLD + "Enter a number between 1 and 8 (inclusive)!" + RESET)
        else:
          getX = False
          getY = False
          break
      if getX == False and getY == False:
        break

    #Catches input exception
    except ValueError:
      print(RED + BOLD + "Enter a valid integer!" + RESET)
      
  return posX, posY # returns the x and y coordinates

#Gets the orientation and checks if it is valid on the board
def getOrientation():
  while True:
    try: # gets a valid orientation (1, 2, 3, or 4)
      orientation = int(input("How would you like the orientation of the boat to be? Enter 1 for right, 2 for up, 3 for left, and 4 for down\n"))
      if orientation < 1 or orientation > 4:
        print(RED + BOLD + "Enter 1, 2, 3, or 4!" + RESET)
      else:
        break

    # Catches input exception
    except ValueError:
      print(RED + BOLD + "Enter a valid integer!" + RESET)

  return orientation

#This function allows the user to place their boats on the grid
def placeBoatsPlayer():
  global userGrid
  
  for i in range(len(ships)): # goes through each of the ships
    orientation = 0
    posX = 0
    posY = 0
    length = ships[i] # gets the length of the current ship
    symbol = shipSymbols[i] # gets the symbol of the current ship
    clearConsole()
    print("Your grid:")
    printBoards("U")
    print(GREEN + BOLD + "ENTER INFO FOR SHIP WITH LENGTH " + str(length) + RESET)
    # get x and y position
    posX, posY = getCoordinates("P", shipNames[i])

    while userGrid[8-posY][posX] != 0: # checks if there is a boat in the coordinates they enters, if so, get new coordinates
      print(RED + BOLD + "Boat exists there, enter new coordinates!" + RESET)
      posX, posY = getCoordinates("P", shipNames[i])
      
    # get orientation
    orientation = getOrientation()

    # check if possible
    while not checkBoatPosition(posX, posY, length, orientation, "U"): # makes sure that the boat has space (not off the grid or colliding wiht other boats)
      print(RED + BOLD + "Ship does not fit, enter new coordinate and orientation information!\n" + RESET)
      # get new coordinate and orientation information
      posX, posY = getCoordinates("P", shipNames[i])
      orientation = getOrientation()

    for i in range(length): # goes through the length of the ship
      # places the boat in the grid depending on the orientation
      userGrid[8-posY][posX] = symbol
      if orientation == 1:
        posX += 1
      elif orientation == 2:
        posY += 1
      elif orientation == 3:
        posX -= 1
      elif orientation == 4:
        posY -= 1

# this function checks if a boat can be placed at the given position and length
def checkBoatPosition(posX, posY, length, orientation, player):
  global oppGrid
  global userGrid
  # check if the boat goes out of the grid
  if orientation==1 and posX + length-1 > 8:
    return False
  if orientation==2 and posY + length-1 > 8:
    return False
  if orientation==3 and posX - length+1 < 1:
    return False
  if orientation==4 and posY - length+1 < 1:
    return False

  if player == "O":
    # check if there is a boat in the way
    for i in range(length):
      if orientation == 1: #right
        if oppGrid[8-posY][posX+i] != 0:
          return False
      if orientation == 2: #up
        if oppGrid[8-posY-i][posX] != 0:
          return False
      if orientation == 3: #left
        if oppGrid[8-posY][posX-i] != 0:
          return False
      if orientation == 4: #down
        if oppGrid[8-posY+i][posX] != 0:
          return False
    
    return True

  if player == "U":
    # check if there is a boat in the way
    for i in range(length):
      if orientation == 1: #right
        if userGrid[8-posY][posX+i] != 0:
          return False
      if orientation == 2: #up
        if userGrid[8-posY-i][posX] != 0:
          return False
      if orientation == 3: #left
        if userGrid[8-posY][posX-i] != 0:
          return False
      if orientation == 4: #down
        if userGrid[8-posY+i][posX] != 0:
          return False
    
    return True

#A function that places the board for the opponent, function works the same as the player placing boats except instead of getting user input, the information is random
def placeBoatsOpp():
  global oppGrid
  for i in range(len(ships)):
    # recieves all the information about the current boat
    orientation = random.randint(1, 4)
    length = ships[i]
    symbol = shipSymbols[i]
    posX = random.randint(1, 8)
    posY = random.randint(1, 8)

    while userGrid[8-posY][posX] != 0: # if the coordinate has a boat there, get new coordinates
      posX = random.randint(1, 8)
      posY = random.randint(1, 8)

    while not checkBoatPosition(posX, posY, length, orientation, "O"): # if the boat is off the screen or colliding with another boat, get new coordinates
      posX = random.randint(1, 8)
      posY = random.randint(1, 8)

    for i in range(length): # goes through the length of the ship
      # places the boat in the grid depending on the orientation
      oppGrid[8-posY][posX] = symbol
      if orientation == 1:
        posX += 1
      elif orientation == 2:
        posY += 1
      elif orientation == 3:
        posX -= 1
      elif orientation == 4:
        posY -= 1

#Prints the game boards
def printBoards(player):
  # we use the global grids (the grid that can be accessed from everywhere) to print the grid
  global userGrid
  global oppGrod
  global oppGridDisplay
  # if we are printing the user board
  if(player == "U"):
    for row in userGrid:
      for spot in row:
        if(str(spot) == "0"):
          print(str(spot) + "\t", end="")
        else:
          print(CYAN + str(spot) + RESET + "\t", end="")
      print("\n")

  # if we are printing the opponent board (the hidden one that contains the boats)
  if(player == "O"):
    for row in oppGrid:
      for spot in row:
        if(str(spot) == "0"):
          print(str(spot) + "\t", end="")
        else:
          print(CYAN + str(spot) + RESET + "\t", end="")
      print("\n")

  if(player == "O2"): # if we are printing the opponent board (the one that the player sees)
    for row in oppGridDisplay:
      for spot in row:
        if(str(spot) == "0"):
          print(str(spot) + "\t", end="")
        else:
          print(CYAN + str(spot) + RESET + "\t", end="")
      print("\n")

#This function handles the user's turn in the game
def userTurn():
  global userMiss
  global oppGrid
  global oppGridDisplay
  posX = 0
  posY = 0

  #Getting coordinate from the user
  posX, posY = getCoordinates("D", "")

  #Checking if they have already played that spot
  while oppGridDisplay[8-posY][posX] == "🔴" or oppGridDisplay[8-posY][posX] == "🔵":
    print(RED + BOLD + "You already played that spot, choose new coordinates!\n" + RESET)
    posX, posY = getCoordinates("D", "")

  # if user misses, replace that spot with a blue circle
  if(oppGrid[8-posY][posX] == 0):
    userMiss = 1
    oppGridDisplay[8-posY][posX] = "🔵"
    oppGrid[8-posY][posX] = "🔵"
  # if user hits, replace that spot with a red circle
  else:
    oppGridDisplay[8-posY][posX] = "🔴"
    oppGrid[8-posY][posX] = "🔴"
    userMiss = 2
  
#This function handles the opponents's turn in the game
def oppTurn():
  global oppMiss
  global userGrid
  global possibleHits
  
  posX = 0
  posY = 0
  spotFound = False

  #Loop to find a spot for the computer to hit
  while not spotFound:
    #If there are no possible spots, guess a random spot
    if not possibleHits:
      #Generating a random spot for the opponent to hit
      while (posX < 1 or posX > 8) or (posY < 1 or posY > 8):
        posX = random.randint(1, 8)
        posY = random.randint(1, 8)
    
      # detects if they have already hit that spot
      while userGrid[8-posY][posX] == "🔴" or userGrid[8-posY][posX] == "🔵":
        posX = random.randint(1, 8)
        posY = random.randint(1, 8)
    
      # if opponent misses, replace that spot with a blue circle
      if(userGrid[8-posY][posX] == 0):
        userGrid[8-posY][posX] = "🔵"
        oppMiss = 1
        spotFound = True
      # if opponent hits, replace that spot with a red circle
      else:
        userGrid[8-posY][posX] = "🔴"
        oppMiss = 2
        #Add adjacent cells to places to hit
        possibleHits.append([posY-1, posX])
        possibleHits.append([posY+1, posX])
        possibleHits.append([posY, posX-1])
        possibleHits.append([posY, posX+1])
        spotFound = True
    else:
      #If there are possible locations where the ship is, continue checking for adjacent cells
      while possibleHits:
        posX = possibleHits[0][1]
        posY = possibleHits[0][0]

        #If the adjacent cell is out of bounds, remove it
        if (posX < 1 or posX > 8) or (posY < 1 or posY > 8):
          possibleHits.pop(0)
          continue

        #If the adjacent cell is already playyed, remove it
        if userGrid[8-posY][posX] == "🔴" or userGrid[8-posY][posX] == "🔵":
          possibleHits.pop(0)
          continue

        #If the spot has no ship, it is a miss
        if userGrid[8-posY][posX] == 0:
          possibleHits.pop(0)
          userGrid[8-posY][posX] = "🔵"
          oppMiss = 1
          spotFound = True
          break
        #If the spot has a ship, clear previous and check for new adjacent cells
        else:
          userGrid[8-posY][posX] = "🔴"
          oppMiss = 2
          possibleHits.clear()
          possibleHits.append([posY-1, posX])
          possibleHits.append([posY+1, posX])
          possibleHits.append([posY, posX-1])
          possibleHits.append([posY, posX+1])
          spotFound = True
          break

#This function checks if any boats are sunken
def checkBoats(grid, turn):
  boatSink1 = True
  boatSink2 = True
  boatSink3 = True
  boatSink4 = True

  #Checks the grid to see if the boat exists and is not sunken
  #If we go through the entire grid and it is not found, the boat is sunk
  for i in range(len(grid[0])):
    for j in range(len(grid)):
      if grid[i][j] == "⛴️":
        boatSink1 = False
      elif grid[i][j] == "🚤":
        boatSink2 = False
      elif grid[i][j] == "⛵":
        boatSink3 = False
      elif grid[i][j] == "🚢":
        boatSink4 = False

  #If it's the user's turn, remove the sunken ship from their current active ships
  if turn == "U":
    if boatSink1 and "⛴️" in userActiveShips:
      userActiveShips.remove("⛴️")
      print(RED + BOLD + "Your battleship has sunk!\n" + RESET)
    if boatSink2 and "🚤" in userActiveShips:
      userActiveShips.remove("🚤")
      print(RED + BOLD + "Your cruiser has sunk!\n" + RESET)
    if boatSink3 and "⛵" in userActiveShips:
      userActiveShips.remove("⛵")
      print(RED + BOLD + "Your submarine has sunk!\n" + RESET)
    if boatSink4 and "🚢" in userActiveShips:
      userActiveShips.remove("🚢")
      print(RED + BOLD + "Your destroyer has sunk!\n" + RESET)

  #If it's the opponent's turn, remove the sunken ship from their current active ships
  else:
    if boatSink1 and "⛴️" in oppActiveShips:
      oppActiveShips.remove("⛴️")
      print(PURPLE + BOLD + "The opponent's battleship has sunk!\n" + RESET)
    if boatSink2 and "🚤" in oppActiveShips:
      oppActiveShips.remove("🚤")
      print(PURPLE + BOLD + "The opponent's cruiser has sunk!\n" + RESET)
    if boatSink3 and "⛵" in oppActiveShips:
      oppActiveShips.remove("⛵")
      print(PURPLE + BOLD + "The opponent's submarine has sunk!\n" + RESET)
    if boatSink4 and "🚢" in oppActiveShips:
      oppActiveShips.remove("🚢")
      print(PURPLE + BOLD + "The opponent's destroyer has sunk!\n" + RESET)

#This function checks if the game is over
def gameOver():
  global quit
  global gameFinished
  
  #Checking if both, the user and computer, has lost all of their ships. It prints the result and quits the game if so
  if not userActiveShips and not oppActiveShips:
    print("\nYou and your opponent have no more ships remaining! It is a tie!\n")
    gameFinished = True
    #Checking if the user has lost all of their ships, prints the result and quits the game if so
  elif not userActiveShips:
    loseImg = climage.convert("lose.png", is_truecolor=True, is_256color=False, is_unicode=True, width=50)
    print(boxing(loseImg, style="double", padding=0, margin=0))
    print(RED + BOLD + "\nYou lost all of your ships! You lose!\n" + RESET)
    print("The opponent's board:\n")
    printBoards("O")
    gameFinished = True
  #Checking if the opponent has lost all of their ships, prints the result and quits the game if so
  elif not oppActiveShips:
    winImg = climage.convert("win.png", is_truecolor=True, is_256color=False, is_unicode=True, width=50)
    print(boxing(winImg, style="double", padding=0, margin=0))
    print(GREEN + BOLD + "\nCongratulations, you won! You successfully sunk of all your opponent's ships!\n" + RESET)
    gameFinished = True

  #If the game is finished, allow the user to return to the menu
  if gameFinished:
    returnToMenu = input(BOLD + "Enter anything to return to the menu:\n" + RESET)
    clearConsole()

#This function displays the help screen for the user
def help():
  clearConsole()
  print("--------------------------------------------")
  print(BOLD + "\n            Welcome to Battleship!             \n" + RESET)
  print("--------------------------------------------")
  print("Battleship is a classic two-player guessing game that requires strategy and a bit of luck. Here, you will be playing against the computer. To begin, both you and the computer will place your ships on separate grids, which is hidden from the other player's view. You will both have 4 ships to place: ")
  print("\n⛴️  battleship --> length of 4")
  print("🚤 cruiser    --> length of 3")
  print("⛵ submarine  --> length of 3")
  print("🚢 destroyer  --> length of 2\n")
  print("You will take turns calling out a grid coordinate to try and hit your opponent's ships. Hits will be indicated with a red circle: '🔴' while misses will be indicated with a blue circle: '🔵'. Your goal is to hit the other players' boats\n")
  print("Once all the coordinates of a ship have been hit, that ship is sunk. The game continues until one player has sunk all of their opponent's ships. It's important to strategize and keep track of where your opponent has already guessed in order to increase your chances of winning.\n\n")
  entMenu = input(BOLD + "Enter anything to go back to the menu!\n" + RESET)
  clearConsole()

def resetGame():
  # used to reset all the global variables we use in the game. This is for if the user chooses to play again
  global userGrid
  global oppGrid
  global oppGridDisplay
  global userMiss
  global oppMiss
  global userActiveShips
  global oppActiveShips
  global gameFinished
  global possibleHits
  
  userGrid = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [" ", 1, 2, 3, 4, 5, 6, 7, 8]
  ]
  oppGrid = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [" ", 1, 2, 3, 4, 5, 6, 7, 8]
  ]
  oppGridDisplay = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [" ", 1, 2, 3, 4, 5, 6, 7, 8]
  ]
  userMiss = 0
  oppMiss = 0
  userActiveShips = ["⛴️", "🚤", "⛵", "🚢"]
  oppActiveShips = ["⛴️", "🚤", "⛵", "🚢"]
  gameFinished = False
  possibleHits = []

while not quit:
  # prints the menu
  title = climage.convert("battleship.png", is_truecolor=True, is_256color=False, is_unicode=True, width=50)
  print(boxing(title, style="double", padding=0, margin=0))
  print("----------------------------------------")
  print("")
  print("               Battleship               ")
  print("")
  print("----------------------------------------")
  print("\n1. Play")
  print("2. Help")
  print("3. Quit")
  # gets whether the user wants to play, get help, or quit
  while True:
    try:
      decision = int(input("\nWhere would you like to go? (Enter the corresponding number to navigate, i.e 1 to play)\n"))
      if decision < 1 or decision > 3:
        print(RED + BOLD + "Enter 1, 2, or 3!" + RESET)
      else:
        break
    except ValueError:
      print(RED + BOLD + "Enter a valid integer!" + RESET)

  #If the user wants to play
  if decision == 1:
    # standard moves at the beginning of a battleship game (reset the board and place boats)
    resetGame() #Resets the game in case player replays the game
    placeBoatsOpp() #Places the boats for the opponent
    placeBoatsPlayer() #Places the boats for the player

    #Game loop
    while not gameFinished:
      # prints the grids
      clearConsole()

      # we would print the opponent's board that contains the boats so we know where their boats are to test lose/win scenarios
      # print("\nOpponent's grid:\n")
      # printBoards("O")
      
      print("\nYour grid:\n")
      printBoards("U")
      
      print("\nOpponent's grid:\n")
      printBoards("O2")
    
      checkBoats(userGrid, "U") # checks if user's boat has sunked
      checkBoats(oppGrid, "O") # checks if opponents's boat has sunked

      # tells the user if they hit or miss
      if userMiss == 1:
        print(RED + BOLD + "YOU MISSED" + RESET)
      elif userMiss == 2:
        print(LIME + BOLD + "YOU HIT" + RESET)

      # tells the user if the opponent hit or miss
      if oppMiss == 1:
        print(LIME + BOLD + "OPPONENT MISSED" + RESET)
      elif oppMiss == 2:
        print(RED + BOLD + "OPPONENT HIT" + RESET)
    
      #Checks if the game has ended
      gameOver()
      #If the game is not finished, continue playing the game
      if not gameFinished:
        userTurn()
        oppTurn()

  #If the user wants to go to help screen
  elif decision == 2:
    help()
    
  #If the user wants to quit
  elif decision == 3:
    quit = True
    clearConsole()
    print("Thanks for playing, see you soon!")