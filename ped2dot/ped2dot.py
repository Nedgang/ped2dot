#!/usr/bin/python3
"""
"""
##########
# IMPORT #
##########
import pandas as pd
from numpy import nan

from .genealogy import Genealogy

#############
# FUNCTIONS #
#############
def ped_to_dot(
    filepath,
    shape_dic={0: "plain", 1: "square", 2: "circle"},
    color_dic={1: "blue", 2: "red", 0: "black"},
):
    """
    Main function used to read pedigree file, create genealogy object for each family
    and then trigger graph creation from it.
    """
    print("Read file:", filepath)
    pedigree = pd.read_csv(
        filepath,
        sep="\t",
        names=["Family", "ID", "Father", "Mother", "Sex", "Phenotype"],
    )
    for family_id in pedigree["Family"].unique():
        create_family_graph(
            pedigree[pedigree["Family"] == family_id], shape_dic, color_dic, family_id
        )


def create_family_graph(family_pedigree, shape_dic, color_dic, family_id):
    genealogy = Genealogy()
    # Reading pedigree file line by line to complete family relationships
    for index, row in family_pedigree.iterrows():
        if row["Father"] is row["Mother"]:
            parents = nan
        else:
            parents = str(row["Father"]) + "_" + str(row["Mother"])

        # Creating individual object if not already existing
        if not genealogy.exist_individual(row["ID"]):
            genealogy.add_individual(row["ID"], row["Sex"], row["Phenotype"], parents)

        # Adding individual to a fertile couple if existing
        if parents is not nan:
            genealogy.add_couple(parents, row["Father"], row["Mother"], row["ID"])

    # Need to plot the tree from top to bottom
    genealogy.create_graph(shape_dic, color_dic, family_id)
