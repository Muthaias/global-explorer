from game.load_node_data import load_yaml

error_views = load_yaml("data/error_views.yaml").get("errors", [])
