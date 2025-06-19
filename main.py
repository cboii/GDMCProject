from gdpc import Editor
from terrain.trees import removeTrees
from maps.featureMaps import MapFeatureExtractor
from maps.visualize import visualize_map_features, visualize_grid
from terrain.terrain_manipulator import TerrainManipulator
from maps.blueprint import Blueprint
from agents.plots import PlotType
from agents.housingAgent import HousingAgent
from agents.coordinator import AgentCoordinator
from buildings.building_module import BuildingModule
import numpy as np


if __name__ == "__main__":
    editor = Editor(buffering=True, bufferLimit=1000000)
    step_size = 32
    gaussian = True
    radius = 2
    border_size = 2

    removeTrees(editor)
    mapFeatures = MapFeatureExtractor(editor)
    # visualize_map_features(mapFeatures)
    blueprint = Blueprint(mapFeatures)
    # visualize_grid(blueprint, step_size=step_size, gaussian=gaussian, radius=radius)
    
    coordinator = AgentCoordinator(blueprint=blueprint, step_size=step_size, gaussian=gaussian, radius=radius)

    coordinator.generate(30, gaussian=gaussian, radius=radius, border_size=border_size)
    blueprint.show()
