class Component:
    """
    Base component class inherited by all other component classes.
    """
    def __init__(self):
        """
        Initialize component.
        """
        pass

    # Sets the components owner to the passed entity.
    def set_owner(self, owner):
        """
        Set the owner of the component.

        owner -- Entity object that owns the component.
        """
        self.owner = owner
