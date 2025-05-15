from gdpc import Editor
from terrain.trees import removeTrees
from maps.featureMaps import MapFeatureExtractor
from maps.visualize import visualize_map_features, visualize_grid
from terrain.terrain_manipulator import TerrainManipulator
from maps.blueprint import Blueprint
from agents.roadAgent import RoadExtendorAgent
from agents.plots import PlotType
from agents.housingAgent import HousingAgent
from agents.coordinator import AgentCoordinator
import numpy as np


if __name__ == "__main__":
    

    editor = Editor(buffering=True)
    step_size = 32
    gaussian = True
    radius = 1

    removeTrees(editor)
    mapFeatures = MapFeatureExtractor(editor)
    visualize_map_features(mapFeatures)
    blueprint = Blueprint(mapFeatures)

    coordinator = AgentCoordinator(blueprint=blueprint, step_size=step_size, gaussian=gaussian, radius=radius)

    coordinator.generate(25, gaussian=gaussian, radius=radius)

    visualize_grid(blueprint, step_size=step_size, gaussian=gaussian, radius=radius)
    blueprint.show()
