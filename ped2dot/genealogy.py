#!/usr/bin/python3
"""
"""
##########
# IMPORT #
##########
from graphviz import Graph

from .couple import Couple
from .individual import Individual

#########
# CLASS #
#########
class Genealogy:
    """
    Object containing all the family individuals, link to each other by family
    relationship.
    """

    def __init__(self):
        self.couples = {}
        self.individuals = {}
        self.generation_max = 0

    def add_couple(self, parents, father, mother, child):
        if self.exist_couple(parents):
            self.couples[parents].add_child(child)
        else:
            self.couples[parents] = Couple(father, mother, child)

    def add_individual(self, name, sex, phenotype, parents):
        if name not in self.individuals:
            self.individuals[name] = Individual(name, sex, phenotype, parents)
        else:
            print("Warning: two individuals have the same ID", name)
            pass

    def exist_individual(self, name):
        return name in self.individuals

    def exist_couple(self, couple_name):
        return couple_name in self.couples

    def compute_generations(self):
        for indiv in self.individuals.items():
            indiv[1].generation = self.compute_individual_generation(indiv[1])
            if indiv[1].generation > self.generation_max:
                self.generation_max = indiv[1].generation

        for couple in self.couples:
            self.couples[couple].generation = max(
                self.individuals[couple.split("_")[0]].generation,
                self.individuals[couple.split("_")[1]].generation,
            )

    def compute_individual_generation(self, indiv):
        if indiv.parents is 0:
            return 0
        elif indiv.generation >= 0:
            return indiv.generation
        else:
            self.individuals[
                indiv.father
            ].generation = self.compute_individual_generation(
                self.individuals[indiv.father]
            )
            self.individuals[
                indiv.mother
            ].generation = self.compute_individual_generation(
                self.individuals[indiv.mother]
            )
            return (
                max(
                    self.individuals[indiv.father].generation,
                    self.individuals[indiv.mother].generation,
                )
                + 1
            )

    def create_graph(self, shape_dic, color_dic, family_id):
        self.compute_generations()
        graph = Graph("Genealogy", format="pdf")
        graph.body.append("splines = ortho; rankdir = TB")
        for generation in range(0, self.generation_max):
            couples = [
                couple[1]
                for couple in self.couples.items()
                if couple[1].generation == generation
            ]
            # Couples node
            subgraph = Graph("Generation {}".format(generation))
            subgraph.attr(rank="same")

            links_progeny = Graph("Links to generation {} progeny".format(generation))

            links_parents = Graph("Links to parental generation")

            progeny_subgraph = Graph("Generation {} progeny".format(generation))
            progeny_subgraph.attr(rank="same")
            for couple in couples:
                subgraph.node(
                    couple.male,
                    shape=shape_dic[self.individuals[couple.male].sex],
                    color=color_dic[self.individuals[couple.male].phenotype],
                )
                subgraph.node(
                    couple.female,
                    shape=shape_dic[self.individuals[couple.female].sex],
                    color=color_dic[self.individuals[couple.female].phenotype],
                )
                subgraph.node(couple.id, shape="point")
                subgraph.edge(couple.male, couple.id)
                subgraph.edge(couple.id, couple.female)

                if couple.nb_children() == 1:
                    progeny_subgraph.node(
                        "progeny_" + couple.children[0], shape="point"
                    )
                    links_progeny.edge(couple.id, "progeny_" + couple.children[0])

                elif couple.nb_children() % 2 == 0:
                    half_children = couple.nb_children() / 2
                    progeny_subgraph.node("progeny_" + couple.id, shape="point")
                    links_progeny.edge(couple.id, "progeny_" + couple.id)
                    for i in range(0, couple.nb_children()):
                        progeny_subgraph.node(
                            "progeny_" + couple.children[i], shape="point"
                        )
                        if i < half_children and i + 1 < half_children:
                            progeny_subgraph.edge(
                                "progeny_" + couple.children[i],
                                "progeny_" + couple.children[i + 1],
                            )
                        elif i < half_children and i + 1 == half_children:
                            progeny_subgraph.edge(
                                "progeny_" + couple.children[i], "progeny_" + couple.id
                            )
                        elif i == half_children and i - 1 < half_children:
                            progeny_subgraph.edge(
                                "progeny_" + couple.id, "progeny_" + couple.children[i]
                            )
                        else:
                            progeny_subgraph.edge(
                                "progeny_" + couple.children[i - 1],
                                "progeny_" + couple.children[i],
                            )

                elif couple.nb_children() % 2 == 1:
                    half_children = couple.nb_children() // 2
                    progeny_subgraph.node(
                        "progeny_" + couple.children[half_children], shape="point"
                    )
                    links_progeny.edge(
                        couple.id, "progeny_" + couple.children[half_children]
                    )
                    for i in range(0, couple.nb_children()):
                        if i == half_children:
                            pass
                        elif i < half_children:
                            progeny_subgraph.node(
                                "progeny_" + couple.children[i], shape="point"
                            )
                            links_progeny.edge(
                                "progeny_" + couple.children[i],
                                "progeny_" + couple.children[i + 1],
                            )
                            pass
                        elif i > half_children:
                            progeny_subgraph.node(
                                "progeny_" + couple.children[i], shape="point"
                            )
                            links_progeny.edge(
                                "progeny_" + couple.children[i - 1],
                                "progeny_" + couple.children[i],
                            )

                if generation > 0:
                    links_parents.edge("progeny_" + couple.male, couple.male)
                    links_parents.edge("progeny_" + couple.female, couple.female)

            graph.subgraph(subgraph)
            if generation > 0:
                graph.subgraph(links_parents)
            graph.subgraph(progeny_subgraph)
            graph.subgraph(links_progeny)

        # To cleanly plot the tree, we need to print the last progenies
        subgraph = Graph("Generation {}".format(self.generation_max))
        links_parents = Graph("Links to parental generation")
        younger_individuals = [
            indiv[1]
            for indiv in self.individuals.items()
            if indiv[1].generation == self.generation_max
        ]
        for indiv in younger_individuals:
            subgraph.node(
                indiv.id, shape=shape_dic[indiv.sex], color=color_dic[indiv.phenotype]
            )
            links_parents.edge("progeny_" + indiv.id, indiv.id)

        graph.subgraph(subgraph)
        graph.subgraph(links_parents)

        graph.render("family_{}.dot".format(family_id), view=True)
