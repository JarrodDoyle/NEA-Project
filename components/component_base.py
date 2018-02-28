class Component:
    # Base component class inherited by all other component classes.
    def __init__(self):
        pass

    # Sets the components owner to the passed entity.
    def set_owner(self, owner):
        self.owner = owner
