import networkx

def cheating():
    G = networkx.DiGraph()

    for a in open("input/day6.txt").readlines(): 
        G.add_edge(*[x.strip() for x in a.split(')')])

    print(networkx.transitive_closure(G).size())

    print(networkx.shortest_path_length(G.to_undirected(), "YOU", "SAN")-2)


cheating()