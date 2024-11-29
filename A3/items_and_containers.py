"""
This program reads files and prints out file contents.
"""

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
    
    def calculate_items_weight(self) -> int:
        """
        Calculate items' total weight.
        """
        items_weight = 0
        for item in self.items:
            items_weight += item.weight
        return items_weight

    def __str__(self) -> str:
        """
        Returns a string representating of the Container.
        @return a string representing the Container.
        """
        return f"{self.name} (total weight: {self.calculate_items_weight() + self.weight}, empty weight: {self.weight}, capacity: {self.calculate_items_weight()}/{self.capacity})"

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

def output() -> None:
    """
    Print out items and containers in a specific format.
    """

    print(f"Initialised {len(items_list)} items including {calculate_number_of_containers()} containers.\n")
    print("Items:")
    for item in items_list:
        if not isinstance(item, Container):
            print(item)
    print()
    print("Containers:")
    for item in items_list:
        if isinstance(item, Container):
            print(item)
    print()

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
        
    output()
