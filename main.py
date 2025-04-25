from gdpc import Editor
from terrain.trees import removeTrees
from maps.featureMaps import MapFeatureExtractor
from maps.visualize import visualize_map_features, visualize_grid
from terrain.terrain_manipulator import TerrainManipulator
from maps.blueprint import Blueprint
from agents.roadAgent import RoadExtendorAgent
from agents.plots import PlotType
from agents.housingAgent import HousingAgent
import numpy as np


if __name__ == "__main__":
    

    editor = Editor()
    # removeTrees(editor)
    mapFeatures = MapFeatureExtractor(editor)
    # visualize_map_features(mapFeatures)
    blueprint = Blueprint(mapFeatures)
    blueprint.place([[10, 10]], type=PlotType.HOUSE)
    road_agent = RoadExtendorAgent(blueprint)
    house_agent = HousingAgent(blueprint)

    for i in range(20):
        try:
            house_agent.find_suitable_build_areas(execute=True)
        except IndexError:
            break
        except ValueError:
            print("none placed")
    
    blueprint.show()

    step_size = 16
    gaussian = True
    radius = 2
    visualize_grid(blueprint, step_size=step_size, gaussian=gaussian, radius=radius)
    tm = TerrainManipulator(blueprint)
    # tm.place_plateau_at_town_center(gaussian=gaussian, step_size=step_size, radius=radius)
