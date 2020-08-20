#!/usr/bin/python3
"""
"""
##########
# IMPORT #
##########
from numpy import nan

#########
# CLASS #
#########
class Individual:
    """
    """

    def __init__(self, name, sex, phenotype, parents):
        self.id = name
        self.sex = sex
        self.phenotype = phenotype
        self.parents = parents
        self.generation = -1
        if self.parents is not nan:
            self.father = parents.split("_")[0]
            self.mother = parents.split("_")[1]
