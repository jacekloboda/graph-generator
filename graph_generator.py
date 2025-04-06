from random import randint
import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(G, directed=False, weighted=False):

    #  defining graph type
    if directed:
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()

    # adding edges to graph
    for i, edges in enumerate(G):
        for edge in edges:
            if weighted and isinstance(edge, tuple):
                graph.add_edge(i, edge[0], weight=edge[1])
            else:
                graph.add_edge(i, edge)

    # positions for nodes
    pos = nx.spring_layout(graph, seed=42)  # seed for relaiability

    # drawing graph
    plt.figure(figsize=(10, 8))

    # node colors
    node_colors = [(0.7, 0.8, 0.9) for _ in graph.nodes()]

    # node size
    node_sizes = [500 + 100 * graph.degree(node) for node in graph.nodes()]

    # drawing nodes
    nx.draw_networkx_nodes(graph, pos,
                           node_color=node_colors,
                           node_size=node_sizes)

    # drawing edges
    nx.draw_networkx_edges(graph, pos,
                           width=2,
                           edge_color='gray',
                           arrows=directed,
                           arrowsize=20)

    # drawing node labels
    nx.draw_networkx_labels(graph, pos,
                            font_size=12,
                            font_weight='bold')

    # drawing edge weughts for weightes graph
    if weighted:
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos,
                                     edge_labels=edge_labels,
                                     font_color='red')

    # adding title
    title = []
    if directed:
        title.append("Directed")
    else:
        title.append("Undirected")
    if weighted:
        title.append("Weighted")
    plt.title(" ".join(title) + " Graph", fontsize=14)

    # turning axis off
    plt.axis('off')

    # showing graph
    plt.tight_layout()
    plt.show()


def bool_stat_input(arg):

    val = input("Generate " + arg + " Graph?(Y/n): ")

    match val.lower():

        case "y": return True

        case "n": return False

        case _:
            print("Wrong format try again")
            return bool_stat_input(arg)

    return


def int_stats_input(arg):

    val = input("Number of " + arg + ": ")

    if not val.isnumeric():

        print("Wrong format try again")
        int_stats_input(arg)

    return int(val)


def enter_limits():

    m = M = ' '

    try:

        m = input("Enter lower limit of weights: ")
        M = input("Enter upper limit of weights: ")

    except ValueError:

        print("Wrong format try again")
        enter_limits()

    if not (m.isnumeric() and M.isnumeric()):

        print("Wrong format try again")
        enter_limits()

    return int(m), int(M)


def graph():

    con = bool_stat_input("Connected")
    direc = bool_stat_input("Directed")
    wght = bool_stat_input("Weightened")

    m_wght, M_wght = enter_limits() if wght else (1, 1)

    node_num = int_stats_input("Nodes")
    edge_num = int_stats_input("Edges")

    G = [[] for _ in range(node_num)]  # list of neighbors of every node

    # randomizing egdes

    if con and (edge_num < node_num-1):  # cant connect every node

        print("This graph is imposible to make")
        return

    edge_cnt = 0  # to keep track how many edges were generated

    if con:  # building simple minimal spanning tree

        while edge_cnt < node_num-1:

            if wght:  # if weightened

                weight = randint(m_wght, M_wght)
                G[edge_cnt].append((edge_cnt+1, weight))

                if not direc:

                    G[edge_cnt+1].append((edge_cnt, weight))

            else:

                G[edge_cnt].append(edge_cnt+1)

                if not direc:

                    G[edge_cnt+1].append(edge_cnt)

            edge_cnt += 1

    while edge_cnt < edge_num:

        parent = randint(0, node_num-1)
        child = randint(0, node_num-1)

        if parent == child:  # i dont want to generate singletons

            continue

        if wght:  # edges are weightened

            weight = randint(m_wght, M_wght)

            if (parent, weight) in G[parent]:  # avioding duplicates
                continue

            G[parent].append((child, weight))

            if not direc:  # edges are not directed
                G[child].append((parent, weight))

        else:  # not weightened

            if child in G[parent]:
                continue  # avoiding duplicates

            G[parent].append(child)
            if not direc:  # edges are not directed
                G[child].append(parent)

        edge_cnt += 1

    # all edges were generated

    for edges in G:
        print(edges)

    draw_graph(G, directed=direc, weighted=wght)

    return G


graph()
