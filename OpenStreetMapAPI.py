import osmnx as ox

def get_roads(point, radius, plot = False):
    G = ox.graph_from_point(point, network_type="drive", dist=radius)

    G_proj = ox.project_graph(G)
    G2 = ox.consolidate_intersections(G_proj, rebuild_graph=True, tolerance=15, dead_ends=False)

    if plot:
        ox.plot_graph(G2, edge_color="blue")

    nodes, edges = ox.graph_to_gdfs(G2)
    return nodes, edges

if __name__ == '__main__':
    point = 59.34318, 18.05141
    radius = 1000

    intersections, roads = get_roads(point, radius, plot = True)

    print(roads.iloc[0]['geometry'])

    