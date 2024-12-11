import osmnx as ox

# Define your bounding box coordinates
north, south, east, west = 40.712200011529475, 40.7122, -74.04449999347214, -74.0445  # Example: Manhattan, NY

# Fetch street network within the bounding box
G = ox.graph_from_bbox([north, south, east, west], network_type='drive')

# Extract node and edge data
node_df = ox.graph_to_gdfs(G, nodes=True)
edge_df = ox.graph_to_gdfs(G, edges=True)

# Filter edges representing streets
street_edges = edge_df[edge_df['highway'] != 'footway']

# Extract coordinates of street segments
street_coords = []
for _, row in street_edges.iterrows():
    geom = row['geometry']
    coords = list(geom.coords)
    street_coords.extend(coords)

# Print or visualize the extracted coordinates
print(street_coords)

# Visualize the extracted street network (optional)
ox.plot_graph(G)