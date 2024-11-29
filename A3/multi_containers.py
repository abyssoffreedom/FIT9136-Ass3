""" 
This program can store looted items into a multi_container and list these items and compartments where they're stored.
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
        Returns a string representing for the Item.
        @return a string representing the Item.
        """

        return f"{self.name} (weight: {self.weight})"


class Container(Item):
    """
    A representation of a Container.
    """
    
    def __init__(self, name: str, weight: int = 0, capacity: int = 0, items: list = []) -> None:
        """
        Create a Container with name, weight, capacity, a list of items.
        """

        super().__init__(name, weight)
        self.capacity = capacity
        self.items = items

    def add_item(self, item: Item) -> None:
        """
        Add an item into the container.
        """

        if item.weight <= self.get_remaining_capacity():
            self.items.append(item)
        else:
            #If the container is full, then raise an OutOfCapacity exception.
            raise OutOfCapacity

    def calculate_used_capacity(self) -> int:
        """
        Calculate the used capacity of the container.
        """

        used_capacity = 0
        for item in self.items:
            if isinstance(item, Container):
                used_capacity += item.calculate_total_weight()
            else:
                used_capacity += item.weight
        return used_capacity

    def calculate_total_weight(self) -> int:
        """
        Calculate a container's total weight.
        @return an integer representing the container's total weight.
        """

        total_weight = self.weight
        # the total weight of the outermost container 
        # will be the sum of its inner items'(which may also be containers) total weight.
        for item in self.items:
            # if item is an instance of Container or its subclass
            if isinstance(item, Container):
                total_weight += item.calculate_total_weight()
            # if item is just an item
            else:
                total_weight += item.weight
        return total_weight

    def get_remaining_capacity(self) -> int:
        """
        Return the remaining capacity of the container.
        @return an integer representing the remaining capacity.
        """
        
        return self.capacity - self.calculate_used_capacity()

    def display(self, indent: int = 0) -> None:
        """
        Print out the container and its contents.
        """

        #Print the string representation of a container with the corresponding indentation.
        #Notice that the __str__() method is overridden in every subclass of Container.
        #So the string representation will change according to the instance that is calling it.
        print("   " * indent + self.__str__())
        #Item in the list of items can either be an instance of Item
        #or that of Container as well as Container's subclass.
        for item in self.items:
            #If item is an instance of Container or its subclass.
            if isinstance(item, Container):
                #Invoke the method itself with indent plus one.
                #If the item is an instance of subclass, it invokes this method by inheriting from Container class.
                item.display(indent + 1)
            #If item is an instance of Item.
            else:
                print("   " * (indent + 1) + item.__str__())

    def __str__(self) -> str:
        """
        Returns a string representing for the Container.
        @return a string representing the Container.
        """

        return f"{self.name} (total weight: {self.calculate_total_weight()}, empty weight: {self.weight}, capacity: {self.calculate_used_capacity()}/{self.capacity})"


class MultiContainer(Container):
    """
    A representation of a Container.
    """
    
    def add_item(self, item: Item) -> None:
        """
        Add an item into the multicontainer.
        """

        for compartment in self.items:
            try:
                compartment.add_item(item)
                return
            except OutOfCapacity:
                continue
        #If each compartment is full, raise OutOfCapacity Exception.
        raise OutOfCapacity
    
    def calculate_empty_weight(self) -> int:
        """
        Calculate a multiContainer's empty weight.
        """

        empty_weight = 0
        for compartment in self.items:
            empty_weight += compartment.weight
        return empty_weight
    
    def __str__(self) -> str:
        """
        Returns a string representing for the Multicontainer.
        @return a string representing the Multicontainer.
        """

        return f"{self.name} (total weight: {self.calculate_total_weight()}, empty weight: {self.calculate_empty_weight()}, capacity: 0/{self.capacity})"


class NameNotFound(Exception):
    """
    A representation of a NameNotFound type exception.
    """
    pass

class OutOfCapacity(Exception):
    """
    A representation of an OutOfCapacity type exception.
    """
    pass

def read_csv(filename: str) -> None:
    """
    Create instances with these information by reading from csv files.
    """

    with open(filename, "r") as ref_file:
        lines = ref_file.readlines()
        #The first line of file is columns' names.
        for line in sorted(lines[1:]):
            vals = line.strip().split(",")
            if filename == "items.csv":
                items_list.append(Item(vals[0], int(vals[1])))
            elif filename == "containers.csv":
                items_list.append(Container(vals[0], int(vals[1]), int(vals[2])))
            else:
                compartments_list = []
                #The first element in vals is MultiContainer's name.
                for val in vals[1:]:
                    #For each container's name, we copy a same-name container from items_list, 
                    #and add it into compartments_list.
                    compartments_list.append(copy_item(val.strip()))
                #For each line in multicontainer's file, we create an instance ofmultiContainer with compartments_list,
                #and add this multiContainer to the items list.
                items_list.append(MultiContainer(name = vals[0], items = compartments_list))

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

    container.display()
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
    files_list = ["items.csv", "containers.csv", "multi_containers.csv"]

    for filename in files_list:
        read_csv(filename)

    start_up()
