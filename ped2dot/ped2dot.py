#!/usr/bin/python3
"""
Main functions, used to parse pedigree file, create and populate genealogy,
and trigger the graph creation.
"""
##########
# IMPORT #
##########
import pandas as pd
import yaml

from .genealogy import Genealogy

#############
# FUNCTIONS #
#############
def ped_to_dot(filepath, config_path):
    """
    Main function used to read pedigree file, and create genealogy for each family.
    """

    print("Reading file:", filepath)
    pedigree = pd.read_csv(
        filepath,
        sep="\t",
        names=["Family", "ID", "Father", "Mother", "Sex", "Phenotype"],
    )
    pedigree = pedigree.fillna(0)

    # Extracting configuration from the configuration file
    cfg = yaml.load(open(config_path, "r"), Loader=yaml.Loader)
    cfg_shape = cfg["shapes"]
    cfg_color = cfg["colors"]
    cfg_graph = cfg["graph_configuration"]

    # Creating a graph for each family
    for family_id in pedigree["Family"].unique():
        create_family_graph(
            pedigree[pedigree["Family"] == family_id],
            cfg_graph,
            cfg_shape,
            cfg_color,
            family_id,
        )


def create_family_graph(family_pedigree, cfg_graph, cfg_shape, cfg_color, family_id):
    """
    Function used to populate genealogy and initiate the graph creation.
    """
    genealogy = Genealogy()
    # Reading pedigree file line by line to complete family relationships
    for index, row in family_pedigree.iterrows():
        if row["Father"] is row["Mother"]:
            parents = 0
        else:
            parents = str(row["Father"]) + "_" + str(row["Mother"])

        # Creating individual object if not already existing
        if not genealogy.exist_individual(row["ID"]):
            genealogy.add_individual(row["ID"], row["Sex"], row["Phenotype"], parents)

        # Adding individual to a fertile couple if existing
        if parents != 0:
            genealogy.add_couple(parents, row["Father"], row["Mother"], row["ID"])

    # Need to plot the tree from top to bottom
    genealogy.create_graph(cfg_graph, cfg_shape, cfg_color, family_id)
