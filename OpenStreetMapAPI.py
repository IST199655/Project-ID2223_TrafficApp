import osmnx as ox

def get_roads(point, radius, plot = False):
    G = ox.graph_from_point(point, network_type="drive", dist=radius)

    G_proj = ox.project_graph(G)
    G2 = ox.consolidate_intersections(G_proj, rebuild_graph=True, tolerance=15, dead_ends=False)

    if plot:
        ox.plot_graph(G2, edge_color="blue")

    nodes, edges = ox.graph_to_gdfs(G2)
    edges = edges.to_crs(epsg=4326)
    return edges

def get_middle_of_roads(edges):
    edges['fraction'] = 0.5
    edges['midpoint_coords'] = edges.apply(
        lambda row: row['geometry'].interpolate(row['fraction'] * row['length']),
        axis=1
    )
    edges = edges.drop(['fraction'], axis = 1)
    return edges

def get_grid(point, radius):
    roads = get_roads(point, radius)

    roads = get_middle_of_roads(roads)

    return roads['midpoint_coords'].to_list()

if __name__ == '__main__':
    coordinates = 59.34318, 18.05141 # Stockholm
    radius = 1000

    grid = get_roads(coordinates, radius, plot = True)

    print(grid)
    print()

    