# Telium – The game

import random
import turtle
import time

# Global variables

num_modules = 17  # The number of modules in the space station
module = 1  # The module of the space station we are in
last_module = 0  # The last module we were in
possible_moves = []  # List of the possible moves we can make
alive = True  # Whether the player is alive or dead
won = False  # Whether the player has won
power = 100  # The amount of power the space station has
fuel = 500  # The amount of fuel the player has in the flamethrower
locked = 0  # The module that has been locked by the player
queen = 0  # Location of the queen alien
vent_shafts = []  # Location of the ventilation shaft entrances
info_panels = []  # Location of the information panels
workers = []  # Location of the worker aliens
previously_locked = []  # Locked modules


# Procedure declarations

def load_module():  # This function loads the modules.
    global module, possible_moves
    possible_moves = get_modules_from(module)
    output_module()


def get_modules_from(module):  # This function opens the text files and finds the possible moves from each movdule.
    moves = []
    text_file = open("Charles_Darwin\module" + str(module) + ".txt", "r")
    for counter in range(0, 4):
        move_read = text_file.readline()
        move_read = int(move_read.strip())
        if move_read != 0:
            moves.append(move_read)
    text_file.close()
    return moves


def output_module():  # This function prints which module the player is in and adds basic decorations.
    global module
    print()
    print("-----------------------------------------------------------------")
    print()
    print("You are in module", module, ".")
    if module == queen:
        print()
        print("There is a queen in here...")
    elif module in workers:
        print()
        print("There are workers in here...")
    elif module in vent_shafts:
        print()
        print("There are vent shafts in here...")
    elif module in info_panels:
        print()
        print("There are info panels in here...")
    print()
    if fuel < 100:
        print("LOW FUEL WARNING!")


def output_moves():  # This function prints the possible modules the player may move to.
    global possible_moves
    print()
    print("From here you can move to modules: | ", end='')
    for move in possible_moves:
        print(move, '| ', end='')
    print()


def get_action():  # This function gets what the player wants to do and where the player wants to move.
    global module, last_module, possible_moves
    valid_action = False
    while not valid_action:
        print("What do you want to do next ? (MOVE + MODULE, FUEL, SCANNER, POWER, LIFEFORMS, INFO, MAP)")
        action = input(">")
        action_modified = (''.join((item for item in action if not item.isdigit()))).replace(" ", "")
        if action_modified.upper() == "MOVE" or action_modified.upper() == "M":
            move = int(''.join((item for item in action if not item.isalpha())))
            if move in possible_moves:
                valid_action = True
                last_module = module
                module = move
            else:
                print("The module must be connected to the current module.")
        elif action_modified.upper() == "SCANNER":
            command = input("Scanner ready. Enter command (LOCK):")
            if command.upper() == "LOCK":
                lock()
        elif action_modified.upper() == "POWER":
            print("The space station has:", power, "power.")
            print("-----------------------------------------------------------------")
        elif action_modified.upper() == "LIFEFORMS":
            print("Worker aliens are located in modules:", workers)
            input("Press any button to continue...")
            print("-----------------------------------------------------------------")
        elif action_modified.upper() == "FUEL":
            print("You have:", fuel, "in your flamethrower.")
            input("Press any button to continue...")
            print("-----------------------------------------------------------------")
        elif action_modified.upper() == "MAP":
            wn = turtle.Screen()
            wn.bgpic('map.gif')
            wn.mainloop()
        elif action_modified.upper() == "INFO":
            print("Ventilation shafts are located in modules:", vent_shafts)
            print("Information panels are located in modules:", info_panels)
            print("You are in module", module, ".")
            input("Press any button to continue...")
            print("-----------------------------------------------------------------")


def spawn_npcs():  # This function spawns NPCS.
    global num_modules, queen, vent_shafts, greedy_info_panels, workers
    module_set = []
    for counter in range(2, num_modules):
        module_set.append(counter)
    random.shuffle(module_set)
    i = 0
    queen = module_set[i]
    for counter in range(0, 3):
        i = i + 1
        vent_shafts.append(module_set[i])

    for counter in range(0, 2):
        i = i + 1
        info_panels.append(module_set[i])

    for counter in range(0, 3):
        i = i + 1
        workers.append(module_set[i])


def check_vent_shafts():  # This function checks if the player is in a module with vent shafts and plays a sequence.
    global num_modules, module, vent_shafts, fuel
    if module in vent_shafts:
        print("There is a bank of fuel cells here.")
        print("You load one into your flamethrower.")
        fuel_gain = [20, 30, 40, 50]  # A list of fuel choices that the player randomly gets.
        fuel_gained = random.choice(fuel_gain)
        print("Fuel was", fuel, "now reading:", fuel + fuel_gained)
        fuel = fuel + fuel_gained
        print("The doors suddenly lock shut.")
        print("What is happening to the station?")
        print("Our only escape is to climb into the ventilation shaft.")
        print("We have no idea where we are going.")
        print("We follow the passages and find ourselves sliding down.")
        input("Press any button to continue...")
        print("-----------------------------------------------------------------")
        last_module = module
        module = random.choice([i for i in range(1, num_modules) if i not in [last_module]])
        load_module()


def check_info_panels():
    global module, info_panels, power
    if module in info_panels:
        if power > 50:
            print("Do you want to use them? It will cost 50 power.")
            action = input(">")
            if action.upper() in ["YES", "YE", "Y"]:
                power -= 50
                print("Loading panel...")
                time.sleep(2)
                input("Loading complete. Press any key to continue...")
                print("-----------------------------------------------------------------")
                print("The queen is in module:", queen)
                print("-----------------------------------------------------------------")
                input("Press any key to continue...")
                print("Shutting down panel...")
                time.sleep(3)
                print("-----------------------------------------------------------------")
            else:
                print("You did not use the info panels...")
        else:
            print("The space station does not have enough power to use them.")


def lock():
    global num_modules, power, locked
    new_lock = int(input("Enter module to lock:"))
    if new_lock < 0 or new_lock > num_modules or new_lock in previously_locked:
        print("Invalid module. Operation failed.")
        input("Press any button to continue...")
        print("-----------------------------------------------------------------")
    elif new_lock == queen:
        print("Operation failed. Unable to lock module.")
        input("Press any button to continue...")
        print("-----------------------------------------------------------------")
    else:
        locked = new_lock
        previously_locked.append(new_lock)
        print("Aliens cannot get into module", locked)
        input("Press any button to continue...")
        print("-----------------------------------------------------------------")
    power_used = 10 + 5 * random.randint(0, 5)
    power -= power_used


def battle():
    global alive, won
    print("The queen is trapped...but you must kill her...")
    input("Press any key to continue...")
    print("-----------------------------------------------------------------")
    while alive and not won:  # START OF BATTLE GAME
        winner = None
        player_health = 100
        queen_health = 100

        # Determine whose turn it is.
        turn = random.randint(1, 2)  # heads or tails
        if turn == 1:
            player_turn = True
            queen_turn = False
            print("\nPlayer will go first.")
        else:
            player_turn = False
            queen_turn = True
            print("\nQueen will go first.")

        print("\nPlayer health: ", player_health, "Queen health: ", queen_health)

        # Set up the main game loop.
        while player_health != 0 or queen_health != 0:

            heal_up = False  # Determine if heal has been used by the player. Resets false each loop.
            miss = False  # Determine if the chosen move will miss.

            # Create a dictionary of the possible moves and randomly select the damage it does when selected.
            moves = {"Burn": random.randint(18, 25),
                     "Mega Burn": random.randint(8, 35),
                     "Heal": random.randint(20, 25)}

            if player_turn:
                print(
                    "\nPlease select a move:\n1. Burn (Deal damage between 18-25)\n2. Mega Burn (Deal damage between "
                    "8-35)\n3. Heal (Restore between 20-25 health)\n")

                player_move = input("> ").lower()

                move_miss = random.randint(1, 8)
                if move_miss == 1:
                    miss = True
                else:
                    miss = False

                if miss:
                    player_move = 0  # The player misses and deals no damage.
                    print("You missed!")
                else:
                    if player_move in ("1", "punch"):
                        player_move = moves["Burn"]
                        print("\nYou used Burn. It dealt ", player_move, " damage.")
                    elif player_move in ("2", "mega punch"):
                        player_move = moves["Mega Burn"]
                        print("\nYou used Mega Burn. It dealt ", player_move, " damage.")
                    elif player_move in ("3", "heal"):
                        heal_up = True  # Heal activated.
                        player_move = moves["Heal"]
                        print("\nYou used Heal. It healed for ", player_move, " health.")
                    else:
                        print("\nThat is not a valid move. Please try again.")
                        continue

            else:  # Queen's turn.

                move_miss = random.randint(1, 5)
                if move_miss == 1:
                    miss = True
                else:
                    miss = False

                if miss:
                    queen_move = 0  # The queen misses and deals no damage.
                    print("The queen missed!")
                else:
                    if queen_health > 30:
                        if player_health > 75:
                            queen_move = moves["Burn"]
                            print("\nThe queen used Burn. It dealt ", queen_move, " damage.")
                        elif 35 < player_health <= 75:  # The queen decides whether to go big or play it safe.
                            imoves = ["Burn", "Mega Burn"]
                            imoves = random.choice(imoves)
                            queen_move = moves[imoves]
                            print("\nThe queen used ", imoves, ". It dealt ", queen_move, " damage.")
                        elif player_health <= 35:
                            queen_move = moves["Mega Burn"]
                            print("\nThe queen used Mega Burn. It dealt ", queen_move, " damage.")
                    else:  # Ff the queen has less than 30 health, there is a 50% chance they will heal.
                        heal_or_fight = random.randint(1, 2)
                        if heal_or_fight == 1:
                            heal_up = True
                            queen_move = moves["Heal"]
                            print("\nThe queen used Heal. It healed for ", queen_move, " health.")
                        else:
                            if player_health > 75:
                                queen_move = moves["Burn"]
                                print("\nThe queen used Burn. It dealt ", queen_move, " damage.")
                            elif 35 < player_health <= 75:
                                imoves = ["Burn", "Mega Burn"]
                                imoves = random.choice(imoves)
                                queen_move = moves[imoves]
                                print("\nThe queen used ", imoves, ". It dealt ", queen_move, " damage.")
                            elif player_health <= 35:
                                queen_move = moves["Mega Burn"]  # FINISH IT!
                                print("\nThe queen used Mega Burn. It dealt ", queen_move, " damage.")

            if heal_up:
                if player_turn:
                    player_health += player_move
                    if player_health > 100:
                        player_health = 100  # cap max health at 100. No over healing!
                else:
                    queen_health += queen_move
                    if queen_health > 100:
                        queen_health = 100
            else:
                if player_turn:
                    queen_health -= player_move
                    if queen_health < 0:
                        queen_health = 0  # cap minimum health at 0
                        winner = "Player"
                        break
                else:
                    player_health -= queen_move
                    if player_health < 0:
                        player_health = 0
                        winner = "Queen"
                        break

            print("\nPlayer health: ", player_health, "Queen health: ", queen_health)

            # Switch turns
            player_turn = not player_turn
            queen_turn = not queen_turn

        if winner == "Player":
            print("\nPlayer health: ", player_health, "Queen health: ", queen_health)
            print("\nThe queen died...")
            won = True
        else:
            print("\nPlayer health: ", player_health, "Queen health: ", queen_health)
            print("\nYou died...")
            alive = False  # END OF BATTLE GAME


def move_queen():
    global alive, num_modules, module, last_module, locked, queen, won, vent_shafts
    # If we are in the same module as the queen...
    if module == queen:
        print("There it is! The queen alien is in this module...")
        # Decide how many moves the queen should take
        moves_to_make = random.randint(1, 3)
        can_move_to_last_module = False
        while moves_to_make > 0:
            # Get the escapes the queen can make
            escapes = get_modules_from(queen)
            # Remove the current module as an escape
            if module in escapes:
                escapes.remove(module)
            # Allow queen to double back behind us from another module
            if last_module in escapes and can_move_to_last_module == False:
                escapes.remove(last_module)
            # Remove a module that is locked as an escape
            if locked in escapes:
                escapes.remove(locked)
            # If there is no escape then player has won...
            if len(escapes) == 0:
                moves_to_make = 0
                print("...and the door is locked. It's trapped.")
                if fuel > 99:
                    battle()
                else:
                    print("You don't have enough fuel to fight...")
                    print("The queen killed you.")
                    alive = False

            # Otherwise move the queen to an adjacent module
            else:
                if moves_to_make == 1:
                    print("...and has escaped.")
                queen = random.choice(escapes)
                moves_to_make = moves_to_make - 1
                can_move_to_last_module = True
                # Handle the queen being in a module with a ventilation shaft
                while queen in vent_shafts:
                    if moves_to_make > 1:
                        print("...and has escaped.")
                    print("We can hear scuttling in the ventilation shafts.")
                    valid_move = False
                # Queen cannot land in a module with another ventilation shaft
                while valid_move == False:
                    valid_move = True
                    queen = random.randint(1, num_modules)
                    if queen in vent_shafts:
                        valid_move = False
                # Queen always stops moving after travelling through shaft
                moves_to_make = 0


def intuition():
    global possible_moves, workers, vent_shafts, info_panels
    for connected_module in possible_moves:
        if connected_module in workers:
            print("I can hear something scuttling!")
            break
        if connected_module in vent_shafts:
            print("I can feel cold air!")
            break
        if connected_module == queen:
            print("Listen! Did you hear that?")
            break
        if connected_module in info_panels:
            print("There is a panel near here. We could use it to find lifeforms.")
            break




# Main program starts here

spawn_npcs()  # Calls the function
print("Ventilation shafts are located in modules:", vent_shafts)
print("Information panels are located in modules:", info_panels)
print("Worker aliens are located in modules:", workers)

while alive and not won:
    load_module()
    check_vent_shafts()
    check_info_panels()
    move_queen()
    if won == False and alive == True:
        intuition()
        output_moves()
        get_action()

if won:
    print("Game over. You win!")
if not alive:
    print("Game Over. You lose.")
