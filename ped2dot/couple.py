#!/usr/bin/python3
#########
# CLASS #
#########
class Couple:
    """
    Couple object, containing id for the two parents and all known children.
    Has an id based on parents id.
    """

    def __init__(self, male, female, child):
        self.id = male + "_" + female
        self.male = male
        self.female = female
        self.children = [child]
        # By default, generation is unknown and must be computed using whole genealogy
        self.generation = -1

    def add_child(self, child_id):
        self.children.append(child_id)

    def nb_children(self):
        return len(self.children)
