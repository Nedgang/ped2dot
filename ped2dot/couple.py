#!/usr/bin/python3
"""
"""
#########
# CLASS #
#########
class Couple:
    """
    """

    def __init__(self, male, female, child):
        self.id = male + "_" + female
        self.male = male
        self.female = female
        self.generation = -1
        self.children = [child]

    def add_child(self, child_id):
        self.children.append(child_id)

    def nb_children(self):
        return len(self.children)
