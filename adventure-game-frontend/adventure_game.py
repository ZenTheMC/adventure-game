import pickle
import tkinter as tk
from tkinter import scrolledtext

# Global variable to hold the output display widget
output_display = None

def display_text(text, style=None):
    global output_display
    output_display.configure(state='normal')
    if style:
        output_display.insert(tk.END, text + '\n', style)
    else:
        output_display.insert(tk.END, text + '\n')
    output_display.configure(state='disabled')
    output_display.see(tk.END)

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}  # Directions to other rooms
        self.items = []  # Items in the room
        self.npcs = []   # NPCs in the room

    def set_exit(self, direction, room, is_locked=False):
        self.exits[direction] = {'room': room, 'locked': is_locked}

    def add_item(self, item):
        self.items.append(item)

    def add_npc(self, npc):
        self.npcs.append(npc)

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Player:
    # Set acceptable directions
    valid_directions = ['north', 'south', 'east', 'west', 'up', 'down']

    def __init__(self, current_room):
        self.current_room = current_room
        self.inventory = []

    def look_at(self, target_name):
        # Check items in the room
        for item in self.current_room.items:
            if item.name.lower() == target_name.lower():
                display_text(f"You look at the {item.name}.")
                display_text(item.description)
                return
        # Check items in inventory
        for item in self.inventory:
            if item.name.lower() == target_name.lower():
                display_text(f"You look at the {item.name} in your inventory.")
                display_text(item.description)
                return
        # Check NPCs in the room
        for npc in self.current_room.npcs:
            if npc.name.lower() == target_name.lower():
                display_text(f"You look at {npc.name}.")
                display_text(npc.description)
                return
        display_text("You don't see that here.")

    def move(self, direction):
        if direction not in self.valid_directions:
            display_text(f"'{direction}' is not a valid direction.")
            display_text("Valid directions are: " + ', '.join(self.valid_directions))
            return
        if direction in self.current_room.exits:
            exit_info = self.current_room.exits[direction]
            if exit_info['locked']:
                if self.has_item('Key'):
                    display_text(f"You use the Key to unlock the door to the {exit_info['room'].name}.")
                    exit_info['locked'] = False
                    self.current_room = exit_info['room']
                    display_text(f"You move to the {self.current_room.name}.", 'bold')
                    self.look()
                else:
                    display_text("The door is locked. You need a key to open it.")
            else:
                self.current_room = exit_info['room']
                display_text(f"You move to the {self.current_room.name}.", 'bold')
                self.look()
        else:
            display_text(f"There is no exit to the {direction} from here.")

    def has_item(self, item_name):
        return any(item.name.lower() == item_name.lower() for item in self.inventory)

    def use_item(self, item_name):
        # Check if the item is in inventory
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                if item.name.lower() == 'flashlight' and self.current_room.name == 'Basement':
                    display_text("You turn on the flashlight and can now see in the dark basement.")
                    # Perhaps reveal hidden items or exits
                    return
                else:
                    display_text(f"You use the {item.name}, but nothing happens.")
                    return
        display_text("You don't have that item.")

    def pick_up(self, item_name):
        for item in self.current_room.items:
            if item.name.lower() == item_name.lower():
                self.inventory.append(item)
                self.current_room.items.remove(item)
                display_text(f"You picked up {item.name}.")
                return
        display_text("Item not found.")

    def look(self):
        display_text(self.current_room.description)
        if self.current_room.npcs:
            display_text("You see:")
            for npc in self.current_room.npcs:
                display_text(f"- {npc.name}")
        if self.current_room.items:
            display_text("You see:")
            for item in self.current_room.items:
                display_text(f"- {item.name}: {item.description}")
        if self.current_room.exits:
            display_text("Exits:")
            for direction in self.current_room.exits:
                display_text(f"- {direction.capitalize()}")
        else:
            if not self.current_room.npcs:
                display_text("There's nothing of interest here.")

    def talk_to(self, npc_name):
        for npc in self.current_room.npcs:
            if npc.name.lower() == npc_name.lower():
                npc.talk(self)
                return
        display_text("There's no one here by that name.")

class NPC:
    def __init__(self, name, dialogue, description="An interesting character."):
        self.name = name
        self.dialogue = dialogue
        self.description = description
        self.quests_given = False

    def talk(self, player):
        if self.name == "Ghost":
            if not self.quests_given:
                display_text(f"{self.name} says: '{self.dialogue}'")
                display_text(f"{self.name} says: 'Bring me the Old Book from the basement!'")
                self.quests_given = True
            else:
                if player.has_item('Old Book'):
                    display_text(f"{self.name} says: 'You have found the book! Thank you!'")
                    player.inventory = [item for item in player.inventory if item.name != 'Old Book']
                    display_text("You gave the Old Book to the Ghost.")
                    # Reward the player
                else:
                    display_text(f"{self.name} says: 'Have you found the Old Book?'")
        else:
            display_text(f"{self.name} says: '{self.dialogue}'")

def main():
    global output_display

    # Create the main window
    root = tk.Tk()
    root.title("Haunted House Adventure")

    # Create the output display
    output_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
    output_display.pack(padx=10, pady=10)
    output_display.configure(state='disabled')

    # Create the input field
    input_field = tk.Entry(root, width=80)
    input_field.pack(padx=10, pady=(0, 10))
    input_field.focus()

    # Set up tags for different text styles
    output_display.tag_configure('bold', font=('TkDefaultFont', 10, 'bold'))

    # Initialize the game world
    # [Initialize rooms, items, NPCs, etc.]
    # Create rooms
    living_room = Room("Living Room", "A cozy living room with a fireplace.")
    kitchen = Room("Kitchen", "A kitchen with a lingering smell of cookies.")
    bedroom = Room("Bedroom", "A small bedroom with a neatly made bed.")
    basement = Room("Basement", "A dark and damp basement.")
    attic = Room("Attic", "A dusty attic filled with old furniture.")

    # Set exits
    living_room.set_exit('north', kitchen)
    kitchen.set_exit('south', living_room)
    living_room.set_exit('east', bedroom, is_locked=True)
    bedroom.set_exit('west', living_room)
    kitchen.set_exit('down', basement)
    basement.set_exit('up', kitchen)
    bedroom.set_exit('up', attic)
    attic.set_exit('down', bedroom)

    # Create items
    key = Item("Key", "A small rusty key.")
    cookie = Item("Cookie", "A freshly baked chocolate chip cookie.")
    flashlight = Item("Flashlight", "A small flashlight. It might be useful in dark places.")
    old_book = Item("Old Book", "An old, dusty book with strange symbols.")

    # Add items to rooms
    kitchen.add_item(cookie)
    bedroom.add_item(key)
    basement.add_item(old_book)
    attic.add_item(flashlight)

    # Create NPCs
    chef = NPC("Chef", "Would you like to try my new recipe?")
    ghost = NPC("Ghost", "Who dares to enter my domain?", "A translucent figure floating in the air.")

    # Add NPCs to rooms
    kitchen.add_npc(chef)
    attic.add_npc(ghost)

    # Create a new room
    garden = Room("Garden", "A lush garden with blooming flowers.")
    bedroom.set_exit('north', garden)
    garden.set_exit('south', bedroom)

    # Add an exit from the Living Room to the Garden
    living_room.set_exit('west', garden)
    garden.set_exit('east', living_room)

    # Create player
    player = Player(living_room)

    # Display introductory text
    display_text("Welcome to the Haunted House Adventure!")
    display_text("You find yourself in an old mansion rumored to be haunted.")
    display_text("Your goal is to explore the house and uncover its secrets.")
    player.look()

    # Define the handle_command function
    def handle_command(event=None):
        command = input_field.get().strip().lower()
        input_field.delete(0, tk.END)
        process_command(command)

    # Bind the Enter key to handle_command
    input_field.bind("<Return>", handle_command)

    # Define process_command function
    def process_command(command):
        nonlocal player  # Since player is defined in main()
        if command in ['quit', 'exit']:
            display_text("Thanks for playing!")
            root.destroy()
        elif command in ['look', 'l', 'examine']:
            player.look()
        elif command.startswith(('look at ', 'examine ', 'look ')):
            if command.startswith('look at '):
                target_name = command[8:]
            elif command.startswith('examine '):
                target_name = command[8:]
            elif command.startswith('look '):
                target_name = command[5:]
            else:
                target_name = ''
            if target_name:
                player.look_at(target_name)
            else:
                player.look()
        elif command.startswith(('go ', 'move ')):
            try:
                direction = command.split(' ')[1]
                player.move(direction.lower())
            except IndexError:
                display_text("Please specify a direction.")
        elif command.startswith('pick up '):
            item_name = command[8:]
            player.pick_up(item_name)
        elif command.startswith('take '):
            item_name = command[5:]
            player.pick_up(item_name)
        elif command.startswith('use '):
            item_name = command[4:]
            player.use_item(item_name)
        elif command in ['inventory', 'i']:
            if player.inventory:
                display_text("You have:")
                for item in player.inventory:
                    display_text(f"- {item.name}: {item.description}")
            else:
                display_text("Your inventory is empty.")
        elif command.startswith(('talk to ', 'talk ')):
            if command.startswith('talk to '):
                npc_name = command[8:]
            else:
                npc_name = command[5:]
            player.talk_to(npc_name)
        elif command == 'save':
            save_game(player)
        elif command == 'load':
            loaded_player = load_game()
            if loaded_player:
                player = loaded_player
                player.look() # Display current room after loading
        elif command == 'help':
            display_text("Available commands:")
            display_text("- look or l: Examine your surroundings.")
            display_text("- look at [object]: Examine an item or NPC.")
            display_text("- go or move [direction]: Move to another room. (e.g., go north)")
            display_text("- pick up or take [item]: Pick up an item. (e.g., pick up key)")
            display_text("- use [item]: Use an item in your inventory.")
            display_text("- talk to [npc]: Talk to a character. (e.g., talk to chef)")
            display_text("- inventory or i: Check your inventory.")
            display_text("- map: Display the game map.")
            display_text("- save: Save the game.")
            display_text("- load: Load a saved game.")
            display_text("- help: Show this help message.")
            display_text("- quit or exit: Exit the game.")
        elif command == 'map':
            show_map()
        else:
            display_text("I don't understand that command.")

    # Create command buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=(0, 10))

    def create_command_button(label, command_text):
        def on_button_click():
            process_command(command_text)
        return tk.Button(button_frame, text=label, command=on_button_click)

    look_button = create_command_button("Look", "look")
    inventory_button = create_command_button("Inventory", "inventory")
    help_button = create_command_button("Help", "help")
    map_button = create_command_button("Map", "map")

    look_button.pack(side=tk.LEFT, padx=5)
    inventory_button.pack(side=tk.LEFT, padx=5)
    help_button.pack(side=tk.LEFT, padx=5)
    map_button.pack(side=tk.LEFT, padx=5)

    # Create the menu bar
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Save Game", command=lambda: save_game(player))
    file_menu.add_command(label="Load Game", command=lambda: load_game())
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    # Start the Tkinter main loop
    root.mainloop()

def show_map():
    display_text("""
        [Attic]
          |
        [Bedroom] - [Garden]
          |
        [Living Room] - [Kitchen]
          |
        [Basement]
    """)

def save_game(player):
    with open('savegame.pkl', 'wb') as f:
        pickle.dump(player, f)
    display_text("Game saved.")

def load_game():
    try:
        with open('savegame.pkl', 'rb') as f:
            player = pickle.load(f)
        display_text("Game loaded.")
        return player
    except FileNotFoundError:
        display_text("No saved game found.")
        return None

if __name__ == "__main__":
    main()