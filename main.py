# Telium – The game

# Imports.
from random import shuffle, choice, randint  # More efficient than importing everything in.
from turtle import Screen
from time import sleep
import csv
from os import system

# Main game variables. Sometimes I use multiple assignments to increase efficiency but I also keep readability.
alive, won = True, False  # Hold whether the player is alive and has won respectively.
power, fuel = 150, 500  # Hold the amount of power and fuel of the station and flame thrower respectively.

# Module variables.
num_modules, module, last_module = 17, 1, 0
# 'num_modules' is the number of total modules. 'module' is the current module the player is in. 'last_module' the player was last in.
locked = 0  # The module that has been locked by the player.
possible_moves = []  # List of the possible moves we can make.
previously_locked = []  # Locked modules.

# NPC variables. All variables here hold the location of the respective NPC.
teleporter, power_distributor, queen = 0, 0, 0
workers, vent_shafts, info_panels = [], [], []

# Other variables.
easter_eggs, previously_vented = [], []


# 'easter_eggs' holds the easter eggs the player has found. 'previously_vented' holds the modules the player has vented.


# Procedure declarations

def load_module():  # This function loads the modules.
    global module, possible_moves
    possible_moves = get_modules_from(module)
    output_module()


def get_modules_from(module):  # This function opens the csv file and finds the possible moves from each module.
    # Using a csv file is more efficient than using .txt files in this case.
    moves = []
    with open('modules.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_line = next(csv_reader)
        pos = first_line.index(str(module))
        for row in csv_reader:
            if int(row[pos]) != 0:  # Ignore '0' module.
                moves.append(int(row[pos]))
    return moves


def output_module():  # This function prints which module the player is in and adds basic decorations.
    global module
    system('cls')
    print("\n-----------------------------------------------------------------\n")
    if module == -1:
        print("Easter egg found!")
        negative_egg = "Module-1 Egg"
        if negative_egg not in easter_eggs:
            easter_eggs.append(negative_egg)

    elif module == 99:
        print("Easter egg found!")
        module99_egg = "Module99 Egg"
        if module99_egg not in easter_eggs:
            easter_eggs.append(module99_egg)
    else:
        print("You are in module", module, ".")
        if module in workers:
            print("\nThere are workers in here...")
        if module in vent_shafts:
            print("\nThere are vent shafts in here...")
        if module in info_panels:
            print("\nThere are info panels in here...")
        if fuel < 100:
            print("LOW FUEL WARNING!")
        print()


def output_moves():  # This function prints the possible modules the player may move to.
    global possible_moves
    print("\nFrom here you can move to modules: | ", end='')
    for move in possible_moves:
        print(move, '| ', end='')
    print()


def get_action():  # This function gets what the player wants to do and where the player wants to move.
    global module, last_module, possible_moves, power, alive
    valid_action = False
    while not valid_action:
        print("What do you want to do next ? (MOVE + MODULE, FUEL, SCANNER, POWER, LIFEFORMS, INFO, MAP, DIE)")
        action = input(">")
        action_modified = (''.join((item for item in action if not item.isdigit()))).replace(" ", "")
        if action_modified.upper() == "MOVE" or action_modified.upper() == "M":
            move = int(''.join((item for item in action if not item.isalpha())))
            if move in possible_moves or move == 99:
                valid_action = True
                last_module = module
                module = move
            else:
                print("The module must be connected to the current module.")
        elif action_modified.upper() == "SCANNER":
            command = input("Scanner ready. Enter command (LOCK, SCAN):")
            if command.upper() == "LOCK":
                lock()
            if command.upper() == "SCAN":
                print("Enter the module you want to scan. It must be connected to your current module.")
                action = 0
                while action not in possible_moves:
                    print(possible_moves)
                    action = int(input(">"))

                if action == queen:
                    print("\nThere is a queen in there...")
                    power -= 25
                    print("25 fuel has been used.")
                    input("Press any button to continue...")
                    print("-----------------------------------------------------------------")
                elif action in workers:
                    print("\nThere are workers in there...")
                    power -= 25
                    print("25 fuel has been used.")
                    input("Press any button to continue...")
                    print("-----------------------------------------------------------------")
                elif action in vent_shafts:
                    print("\nThere are vent shafts in there...")
                    power -= 25
                    print("25 fuel has been used.")
                    input("Press any button to continue...")
                    print("-----------------------------------------------------------------")
                elif action in info_panels:
                    print("\nThere are info panels in there...")
                    power -= 25
                    print("25 fuel has been used.")
                    input("Press any button to continue...")
                    print("-----------------------------------------------------------------")
                else:
                    print("There is nothing in there...")
                    power -= 25
                    print("25 fuel has been used.")
                    input("Press any button to continue...")
                    print("-----------------------------------------------------------------")
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
            wn = Screen()
            wn.bgpic('map.gif')
            wn.mainloop()
        elif action_modified.upper() == "INFO":
            print("Ventilation shafts are located in modules:", vent_shafts)
            print("Information panels are located in modules:", info_panels)
            print("You are in module", module, ".")
            input("Press any button to continue...")
            print("-----------------------------------------------------------------")
        elif action_modified.upper() == "EGG":
            print("Easter egg found!")
            action_egg = "Action Egg"
            if action_egg not in easter_eggs:
                easter_eggs.append(action_egg)
            input("Press any button to continue...")
        elif action_modified.upper() == "DIE":
            system('cls')
            print(r"""            ██████╗ ███████╗███████╗███████╗ █████╗ ████████╗
            ██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗╚══██╔══╝
            ██║  ██║█████╗  █████╗  █████╗  ███████║   ██║   
            ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██╔══██║   ██║   
            ██████╔╝███████╗██║     ███████╗██║  ██║   ██║   
            ╚═════╝ ╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   
                                                             """)
            print("\nGame Over. You lose.")
            input("Press any key to finish...")
            reset()
            print("-----------------------------------------------------------------\n")
            print("-----------------------------------------------------------------\n")
            menu()


def spawn_npcs():  # This function spawns NPCS.
    global num_modules, queen, vent_shafts, greedy_info_panels, workers, power_distributor, teleporter
    module_set = []
    for counter in range(2, num_modules):
        module_set.append(counter)
    shuffle(module_set)
    i = 0
    queen = module_set[i]
    power_distributor = module_set[i + 11]
    teleporter = module_set[i + 12]
    for counter in range(0, 3):
        i = i + 1
        vent_shafts.append(module_set[i])
    for counter in range(0, 2):
        i = i + 1
        info_panels.append(module_set[i])
    for counter in range(0, 5):
        i = i + 1
        workers.append(module_set[i])


def check_vent_shafts():  # This function checks if the player is in a module with vent shafts and plays a sequence.
    global num_modules, module, vent_shafts, fuel, last_module, previously_vented
    if module in vent_shafts:
        if module not in previously_vented:
            print("There is a bank of fuel cells here.")
            print("You load one into your flamethrower.")
            fuel_gain = [20, 30, 40, 50]  # A list of fuel choices that the player randomly gets.
            fuel_gained = choice(fuel_gain)
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
        if randint(1, 100) == 1:
            module = -1
        else:
            module = choice([i for i in range(1, num_modules) if i not in [last_module]])
        load_module()


def check_info_panels():  # This function checks if the player is in a module with info panels and plays a sequence.
    global module, info_panels, power
    if module in info_panels:
        if power > 50:
            print("Do you want to use them? It will cost 50 power.")
            action = input(">")
            if action.upper() in ["YES", "YE", "Y"]:
                power -= 50
                print("Loading panel...")
                sleep(2)
                input("Loading complete. Press any key to continue...")
                print("-----------------------------------------------------------------")
                print("The queen is in module:", queen)
                print("The power distributor is in module:", power_distributor)
                print("-----------------------------------------------------------------")
                input("Press any key to continue...")
                print("Shutting down panel...")
                sleep(3)
                print("-----------------------------------------------------------------")
            else:
                print("You did not use the info panels...")
        else:
            print("The space station does not have enough power to use them.")


def lock():  # This function is for locking modules.
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
    power_used = 10 + 5 * randint(0, 5)
    power -= power_used
    print(power_used, "power has been used.")
    print("Power:", power)


def battle():  # This function is for when the player has their final battle againt the queen.
    global alive, won
    system('cls')
    print("You must kill her...")
    input("Press any key to continue...")
    print("-----------------------------------------------------------------")
    while alive and not won:  # START OF BATTLE
        winner = None
        player_health = 100
        queen_health = 100

        # Determine whose turn it is.
        turn = randint(1, 2)  # heads or tails
        if turn == 1:
            player_turn, queen_turn = True, False
            print("\nPlayer will go first.")
        else:
            player_turn, queen_turn = False, True
            print("\nQueen will go first.")

        print("\nPlayer health:", player_health, "Queen health:", queen_health)

        # Set up the main game loop.
        while player_health != 0 or queen_health != 0:

            heal_up, miss = False, False
            # 'miss' determines if the chosen move will miss. 'heal_up' determines if heal has been used by the player. Resets false each loop.

            # Create a dictionary of the possible moves and randomly select the damage it does when selected.
            moves = {"Blast": randint(18, 25),
                     "Mega Blast": randint(8, 35),
                     "Heal": randint(20, 25)}

            if player_turn:
                print(
                    "\nPlease select a move:\n1. Blast (Deal damage between 18-25)\n2. Mega Blast (Deal damage between "
                    "8-35)\n3. Heal (Restore between 20-25 health)\n")

                player_move = input("> ").lower()

                move_miss = randint(1, 8)
                if move_miss == 1:
                    miss = True
                else:
                    miss = False

                if miss:
                    player_move = 0  # The player misses and deals no damage.
                    print("You missed!")
                else:
                    if player_move in ("1", "punch"):
                        player_move = moves["Blast"]
                        print("\nYou used Blast. It dealt ", player_move, " damage.")
                    elif player_move in ("2", "mega punch"):
                        player_move = moves["Mega Blast"]
                        print("\nYou used Mega Blast. It dealt ", player_move, " damage.")
                    elif player_move in ("3", "heal"):
                        heal_up = True  # Heal activated.
                        player_move = moves["Heal"]
                        print("\nYou used Heal. It healed for ", player_move, " health.")
                    else:
                        print("\nThat is not a valid move. Please try again.")
                        continue

            else:  # Queen's turn.

                move_miss = randint(1, 5)
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
                            queen_move = moves["Blast"]
                            print("\nThe queen used Blast. It dealt ", queen_move, " damage.")
                        elif 35 < player_health <= 75:  # The queen decides whether to go big or play it safe.
                            imoves = choice(["Blast", "Mega Blast"])
                            queen_move = moves[imoves]
                            print("\nThe queen used ", imoves, ". It dealt ", queen_move, " damage.")
                        elif player_health <= 35:
                            queen_move = moves["Mega Blast"]
                            print("\nThe queen used Mega Blast. It dealt ", queen_move, " damage.")
                    else:  # If the queen has less than 30 health, there is a 50% chance they will heal.
                        heal_or_fight = randint(1, 2)
                        if heal_or_fight == 1:
                            heal_up = True
                            queen_move = moves["Heal"]
                            print("\nThe queen used Heal. It healed for ", queen_move, " health.")
                        else:
                            if player_health > 75:
                                queen_move = moves["Blast"]
                                print("\nThe queen used Blast. It dealt ", queen_move, " damage.")
                            elif 35 < player_health <= 75:
                                imoves = choice(["Blast", "Mega Blast"])
                                queen_move = moves[imoves]
                                print("\nThe queen used ", imoves, ". It dealt ", queen_move, " damage.")
                            elif player_health <= 35:
                                queen_move = moves["Mega Blast"]  # FINISH IT!
                                print("\nThe queen used Mega Blast. It dealt ", queen_move, " damage.")

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
            player_turn, queen_turn = not player_turn, not queen_turn

        if winner == "Player":
            print("\nPlayer health: ", player_health, "Queen health: ", queen_health)
            print("\nThe queen died...")
            won = True
        else:
            print("\nPlayer health: ", player_health, "Queen health: ", queen_health)
            print("\nYou died...")
            alive = False  # END OF BATTLE


def move_queen():  # This function is for when the player meets the queen and the queen moves.
    global alive, num_modules, module, last_module, locked, queen, won, vent_shafts
    # If we are in the same module as the queen...
    if module == queen:
        print("There it is! The queen alien is in this module...")
        # Decide how many moves the queen should take
        moves_to_make = randint(1, 3)
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
            for i in range(len(previously_locked)):
                if previously_locked[i] in escapes:
                    escapes.remove(previously_locked[i])

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
                queen = choice(escapes)
                moves_to_make = moves_to_make - 1
                can_move_to_last_module = True
                # Handle the queen being in a module with a ventilation shaft
                while queen in vent_shafts:
                    if moves_to_make > 1:
                        print("...and has escaped.")
                    print("We can hear scuttling in the ventilation shafts.")
                    valid_move = False
                    # Queen cannot land in a module with another ventilation shaft
                    while not valid_move:
                        valid_move = True
                        queen = randint(1, num_modules)
                        if queen in vent_shafts:
                            valid_move = False
                # Queen always stops moving after travelling through shaft
                moves_to_make = 0


def intuition():  # This function is used for when the player is near an NPC.
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


def worker_aliens():  # This function is for when a player encounters a worker alien.
    global module, workers, fuel, alive
    # Output alien encountered
    if module in workers:
        print("Startled, a young alien scuttles across the floor.")
        print("It turns and leaps towards us.")
        # Get the player's action
        successful_attack = False
        while not successful_attack:
            print("You can:\n")
            print("- (B) Blast your flamethrower to frighten it away.")
            print("- (M) Mega Blast your flamethrower to try to kill it.")
            print("- (R) Run away. Note: You might die! \n")
            print("How will you react? (B, M, R)")
            action = 0
            while action not in ["B", "M", "R"]:
                action = input("Press the trigger: ").upper()
            if action == "R":
                print("You decide to run...")
                death = randint(1, 7)
                if death == 1:
                    print("The alien killed you while you tried to run!")
                    input("Press any key to continue...")
                    alive = False
                    return
                else:
                    print()

                if last_module in possible_moves:
                    module = last_module
                    load_module()
                    break
                else:
                    module = choice(possible_moves)
                    load_module()
                    break

            while 1:  # Using 'while 1' is more efficient than using 'while True'
                try:
                    fuel_used = float(input("How much fuel will you use? ..."))
                    if fuel_used <= 0:
                        raise ValueError
                    break
                except ValueError:
                    print("Please type a positive number.")

            fuel = fuel - fuel_used
            # Check if player has run out of fuel
            if fuel <= 0:
                print("You ran out of fuel!")
                print("The worker alien killed you...")
                input("Press any key to continue...")
                alive = False
                return
            # Work out how much fuel is needed
            if action.upper() == "B":
                fuel_needed = 30 + 10 * randint(0, 5)
            if action.upper() == "M":
                fuel_needed = 90 + 10 * randint(0, 5)
            # Try again if not enough fuel was used
            if fuel_used >= fuel_needed:
                successful_attack = True
            else:
                print("The alien squeals but is not dead. It’s angry.")
        # Successful action
        if action.upper() == "B":
            print("The alien scuttles away into the corner of the room.")
        if action.upper() == "M":
            print("The alien has been destroyed.")
            # Remove the worker from the module
            workers.remove(module)
        print()


def check_power_distributor():  # This function is for when a player meets a power distributor.
    global module, fuel, power, power_distributor
    if module == power_distributor:
        print("The power distributor is in this module.")
        print("Would you like to convert flamethrower fuel to power?")
        action = input(">")
        if action.upper() in ["Y", "YES"]:
            while 1:
                try:
                    amount = int(input("How much fuel would you like to convert?:"))
                    if amount <= 0:
                        raise ValueError
                    break
                except ValueError:
                    print("Please type a positive number.")

            if amount < fuel:
                print("Converting fuel...")
                sleep(1)
                print("25% complete")
                sleep(1)
                print("50% complete")
                sleep(1)
                print("75% complete")
                sleep(1)
                print("99% complete")
                sleep(2)
                fuel -= amount
                power += amount
                print("100% complete")
                print("Fuel:", fuel)
                print("Power:", power)
                input("Press any key to continue...")
            else:
                print("ERROR!")
                print("Insufficient fuel amount.")
                input("Press any key to continue...")
        else:
            print("You decided not to convert the fuel...")


def check_teleporter():  # This function is for when a player meets a teleporter.
    global module, teleporter, power, last_module
    if module == teleporter:
        print("You found the teleporter!")
        print("Would you like to teleport to another module? It will use 50 power.")
        action = input(">")
        if action.upper() in ["Y", "YES"]:
            while 1:
                try:
                    tpm = int(input("Which module would you like to teleport to?:"))
                    if tpm > 17 or tpm < 1:
                        raise ValueError
                    break
                except ValueError:
                    print("Please type a valid module.")

            last_module = module
            module = tpm
            power -= 50
            print("Starting teleport...")
            sleep(2)
            load_module()
        else:
            print("You decided not to teleport.")


# Main program starts here

def menu():  # This function is for the pre-game menu.
    system('cls')
    print(r"""████████╗███████╗██╗     ██╗██╗   ██╗███╗   ███╗
╚══██╔══╝██╔════╝██║     ██║██║   ██║████╗ ████║
   ██║   █████╗  ██║     ██║██║   ██║██╔████╔██║
   ██║   ██╔══╝  ██║     ██║██║   ██║██║╚██╔╝██║
   ██║   ███████╗███████╗██║╚██████╔╝██║ ╚═╝ ██║
   ╚═╝   ╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝     ╚═╝
                                                """)  # ANSI Shadow ASCII font.
    print("1. Start")
    print("2. How to play")
    print("3. Credits")
    print("4. Easter eggs")
    while 1:
        try:
            action = int(input(">"))
            if action not in [1, 2, 3, 4, 5]:
                raise ValueError
            break
        except ValueError:
            print("Please type a valid number.")
    if action == 1:
        system('cls')
        print("Loading game...")
        sleep(2)
        input("Press any key to begin...")
        print("-----------------------------------------------------------------\n")
        print("-----------------------------------------------------------------\n")
        main()
    elif action == 2:
        system('cls')
        print(
            "\n Telium is a text-based game which means that you will have to type things in.\n "
            "The objective is to kill the queen who is in one of the 17 modules.\n The queen "
            "has workers which you will also encounter.\n There are additional objects such as "
            "info-panels and vents.\n The queen can escape and so you must use your scanner to "
            "lock certain modules to stop her from escaping. \n You can figure the rest out for yourself!\n "
            "Good luck!\n")
        input("Press any key to return to the main menu...")
        menu()
    elif action == 3:
        system('cls')
        print("Created by Prince.")
        input("Press any key to return to the main menu...")
        menu()
    elif action == 4:
        system('cls')
        print("There are 4 easter eggs in the game. Try to find them all!")
        print("Your current list of easter eggs found:", easter_eggs)
        if len(easter_eggs) == 4:
            print("Congratulations! You have found all the easter eggs! ")
        input("Press any key to return to the main menu...")
        menu()
    elif action == 5:
        system('cls')
        print("Easter egg found!")
        menu_egg = "Menu Egg"
        if menu_egg in easter_eggs:
            input("Press any key to return to the main menu...")
            menu()
        else:
            easter_eggs.append(menu_egg)
        input("Press any key to return to the main menu...")
        menu()


def reset():  # This resets all variables for the next game.
    system('cls')
    global easter_eggs, previously_vented, vent_shafts, info_panels, workers, previously_locked, possible_moves, power, fuel, module, last_module, alive, won, locked, queen, power_distributor, teleporter
    easter_eggs.clear()
    previously_vented.clear()
    vent_shafts.clear()
    info_panels.clear()
    workers.clear()
    previously_locked.clear()
    possible_moves.clear()
    module = 1
    last_module = 0
    alive = True
    won = False
    power = 150
    fuel = 500
    locked = 0
    queen = 0
    power_distributor = 0
    teleporter = 0


def main():
    spawn_npcs()  # Calls the function.
    print("Ventilation shafts are located in modules:", vent_shafts)
    print("Information panels are located in modules:", info_panels)
    print("Worker aliens are located in modules:", workers)

    while alive and not won:
        load_module()
        move_queen()
        if alive and not won:
            check_vent_shafts()
            check_info_panels()
            check_power_distributor()
            check_teleporter()
            worker_aliens()
        if not won and alive:
            intuition()
            output_moves()
            get_action()

    if won:
        system('cls')
        print(r"""            ██╗   ██╗██╗ ██████╗████████╗ ██████╗ ██████╗ ██╗   ██╗
                    ██║   ██║██║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝
                    ██║   ██║██║██║        ██║   ██║   ██║██████╔╝ ╚████╔╝ 
                    ╚██╗ ██╔╝██║██║        ██║   ██║   ██║██╔══██╗  ╚██╔╝  
                     ╚████╔╝ ██║╚██████╗   ██║   ╚██████╔╝██║  ██║   ██║   
                      ╚═══╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
                                                                           """)
        print("Game over. You win!")
        input("Press any key to finish...")
        reset()
        system('cls')
        print("-----------------------------------------------------------------\n")
        print("-----------------------------------------------------------------\n")
        menu()
    if not alive:
        system('cls')
        print(r"""            ██████╗ ███████╗███████╗███████╗ █████╗ ████████╗
                    ██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗╚══██╔══╝
                    ██║  ██║█████╗  █████╗  █████╗  ███████║   ██║   
                    ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██╔══██║   ██║   
                    ██████╔╝███████╗██║     ███████╗██║  ██║   ██║   
                    ╚═════╝ ╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   
                                                                     """)
        print("\nGame Over. You lose.")
        input("Press any key to finish...")
        reset()
        system('cls')
        print("-----------------------------------------------------------------\n")
        print("-----------------------------------------------------------------\n")
        menu()


menu()
