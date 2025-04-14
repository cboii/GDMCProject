from gdpc import Editor
from terrain.trees import removeTrees
from maps.featureMaps import MapFeatureExtractor
from maps.buildMaps import BuildMap
from maps.visualize import visualize_map_features, visualize_grid
from terrain.terrain_manipulator import TerrainManipulator


if __name__ == "__main__":
    editor = Editor()
    # removeTrees(editor)
    mapFeatures = MapFeatureExtractor(editor)
    visualize_map_features(mapFeatures)

    build_map = BuildMap(editor)
    step_size = 16
    gaussian = True
    visualize_grid(build_map, step_size=step_size, gaussian=gaussian)
    tm = TerrainManipulator(editor, build_map)
    tm.place_plateau_at_town_center(gaussian=gaussian, step_size=step_size)
