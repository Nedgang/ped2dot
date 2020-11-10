#!/usr/bin/python3

#########
# CLASS #
#########
class Individual:
    """
    Object used to store all needed information for each individual in the graph.
    """

    def __init__(self, name, sex, phenotype, parents):
        self.id = name
        self.sex = sex
        self.phenotype = phenotype
        self.parents = parents
        self.generation = -1
        if self.parents != 0:
            self.father = parents.split("_")[0]
            self.mother = parents.split("_")[1]
        self.in_couple = False

    def has_parents(self):
        return self.parents != 0

    def has_couple(self):
        self.in_couple = True
