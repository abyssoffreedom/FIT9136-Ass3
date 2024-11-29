"""
This program can store looted items into a capacity and list these items.
"""

import copy

class Item:
    """
    A representation of an item.
    """

    def __init__(self, name: str = "", weight: int = 0) -> None:
        """
        Creates an item with a name and weight.
        """

        self.name = name
        self.weight = weight

    def __str__(self) -> str:
        """
        Returns a string representating of the Item.
        @return a string representing the Item.
        """

        return f"{self.name} (weight: {self.weight})"


class Container(Item):
    """
    A representation of a Container.
    """
    
    def __init__(self, name: str, weight: int = 0, capacity: int = 0, items: list = []) -> None:
        """
        Create a Container with name, weight, capacity, item.
        """

        super().__init__(name, weight)
        self.capacity = capacity
        self.items = items

    def add_item(self, item: Item) -> None:
        """
        Add an item into the container
        """

        if item.weight <= self.get_remaining_capacity():
            self.items.append(item)
        else:
            #If the container is full, then raise an OutOfCapacity exception.
            raise OutOfCapacity

    def calculate_items_weight(self) -> int:
        """
        Calculate items' total weight.
        @return a int representing the items' total weight.
        """

        items_weight = 0
        for item in self.items:
            items_weight += item.weight
        return items_weight

    def get_remaining_capacity(self) -> int:
        """
        Return the remaining capacity of the container.
        @return an int representing the remaining capacity.
        """

        return self.capacity - self.calculate_items_weight()

    def __str__(self) -> str:
        """
        Return a string representating of the Container.
        @return a string representing the Container.
        """

        items_info = ""
        for item in self.items:
            items_info += "\n   " + item.__str__()
        return f"{self.name} (total weight: {self.calculate_items_weight() + self.weight}, empty weight: {self.weight}, capacity: {self.calculate_items_weight()}/{self.capacity}){items_info}"

class NameNotFound(Exception):
    """
    A representation of a NameNotFound type exception.
    """
    pass

class OutOfCapacity(Exception):
    """
    A representating of an OutOfCapacity type exception.
    """
    pass

def read_csv(filename: str) -> None:
    """
    Create instances with these information by reading from csv files.
    """

    with open(filename, "r") as ref_file:
        lines = ref_file.readlines()
        for line in sorted(lines[1:]):
            vals = line.strip().split(",")
            if filename == "items.csv":
                items_list.append(Item(vals[0], int(vals[1])))
            else:
                items_list.append(Container(vals[0], int(vals[1]), int(vals[2])))

def start_up() -> None:
    """
    Start up the game.
    """

    print(f"Initialised {len(items_list)} items including {calculate_number_of_containers()} containers.\n")
    while True:
        container_name = input("Enter the name of the container: ")
        try:
            main_menu(copy_item(container_name))
            return
        except NameNotFound:
            print(f"\"{container_name}\" not found. Try again.")

        
def main_menu(container: Container) -> None:
    """
    Prompts the user to choose next step.
    """

    print("=" * 34)
    print("Enter your choice:")
    print("1. Loot item.")
    print("2. List looted items.")
    print("0. Quit.")
    print("=" * 34)

    choice = input()
    if choice == "1":
        loot_item(container)
    elif choice == "2":
        list_looted_items(container)
    elif choice == "0":
        exit()

def loot_item(container: Container) -> None:
    """
    Add an item input by user to a specific container.
    """
    
    while True:
        item_name = input("Enter the name of the item: ")
        try:
            item = copy_item(item_name)
            try:
                container.add_item(item)
                print(f"Success! Item \"{item_name}\" stored in container \"{container.name}\".")
                break
            except OutOfCapacity:
                print(f"Failure! Item \"{item_name}\" NOT stored in container \"{container.name}\".")
                break
        except NameNotFound:
            print(f"\"{item_name}\" not found. Try again.")
    main_menu(container)
    return

def list_looted_items(container: Container) -> None:
    """
    List looted items in a specific container.
    """

    print(container)
    main_menu(container)
    return

def copy_item(name: str) -> Item:
    """
    Return an item copy, instances of Container included.
    """

    for item in items_list:
        if item.name == name:
            return copy.deepcopy(item)
    #If the item's name is not found in the list, raise a NameNotFound type exception.
    raise NameNotFound

def calculate_number_of_containers() -> int:
    """
    calculate the number of containers in the items list.
    """

    total = 0
    for item in items_list:
        if isinstance(item, Container):
            total += 1
    return total

if __name__ == '__main__':
    #This list will be used to store both items and containers, since we regard container as a kind of item.
    items_list = []
    files_list = ["items.csv", "containers.csv"]

    for filename in files_list:
        read_csv(filename)

    start_up()
