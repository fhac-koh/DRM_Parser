from drm_parser import parser as ps
import matplotlib.pyplot as plt
import networkx as nx

plt.rcParams['font.family'] = 'IPAexMincho'

def main():
    parser = ps()
    text_lines = parser.file_open("./533421.txt")
    classify = parser.detective_classify_id(text_lines)
    nodes, links, locates = parser.parse(classify)

    G = nx.Graph()
    pos = {}
    labeldict = {}
    for node in nodes:
        node_id = node[0][0]
        node_axis = node[0][1]
        G.add_node(node_id, color="red")
        pos[node_id] = tuple(node_axis)
    for link in links:
        inc = 0
        linked_node_id = link[0]
        complements_axis = link[1]
        for complement_axis in complements_axis:
            G.add_node(f"{linked_node_id[0]}to{linked_node_id[1]}_{inc}", color="lightblue")
            pos[f"{linked_node_id[0]}to{linked_node_id[1]}_{inc}"] = tuple(complement_axis)
            if inc == 0:
                G.add_edge(linked_node_id[0], f"{linked_node_id[0]}to{linked_node_id[1]}_{inc}")
            elif inc < len(links)-1:
                G.add_edge(f"{linked_node_id[0]}to{linked_node_id[1]}_{inc-1}", f"{linked_node_id[0]}to{linked_node_id[1]}_{inc}")
            else:
                G.add_edge(f"{linked_node_id[0]}to{linked_node_id[1]}_{inc}", linked_node_id[1])
            inc += 1
    for locate in locates:
        locate_axis = locate[0][0]
        locate_name = locate[0][1]
        if locate_name in G.nodes:
            continue
        G.add_node(locate_name, color="orange")
        pos[locate_name] = tuple(locate_axis)
        labeldict[locate_name] = locate_name

    # nx.draw's node_color is not working(color "red") so commentout below
    # colors = nx.get_node_attributes(G, 'color').values()
    # nx.draw(G, pos, with_labels=True, labels=labeldict, node_color=colors, font_family='IPAexMincho')

    nx.draw(G, pos, with_labels=True, labels=labeldict, font_family='IPAexMincho')
    plt.show()

if __name__ == "__main__":
    main()