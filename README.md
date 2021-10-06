# LogicGatesInGRN

This repository contains code used to find logic gates in gene regulatory networks (GRN), and heavily uses the DSGRN software created by Konstantin Mischaikow's group at Rutgers. That software can be found in the DSGRN repository belonging to Marcio Gameiro. The method of finding logic gates is a generalization of the procedure found in the paper "identifying robust hysteresis in networks".

The program fourCorners takes a single network (with 4 nodes) and computes the percentage of double factor graphs satisfying the four point criterion, as well as the edge criterion. It will then add the particular double factor graph indices to an SQL database.

The program essentialBistableNodes takes a single network and computes the total number of bistable nodes, as well as the number of bistable nodes in each "good" double factor graph (those satisfying the four point and edge criterion). 

As there are hundreds of thousands of graphs, both sets of code were written to be run on a cluster. 

Given the information from these two programs, we can compute a score of "likelihood of behaving like an AND or OR gate". The program NCA uses neighborhood component analysis to learn a 2 dimensional metric so we can see a sort of topology on network space. 

The program Persistence uses the package scikit-tda to complement NCA in trying to give a description of the topology on network space in terms of its likelihood scores. 
