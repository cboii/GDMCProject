import json
import os
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
from buildings.narrative import add_narrative
import numpy as np
from dotenv import load_dotenv
from openAIClient import generate_settlement_story
import openai

if __name__ == "__main__":
    load_dotenv()
    openai.api_key = os.environ["OPENAI_API_KEY"]
    editor = Editor(buffering=True, bufferLimit=1000000)
    step_size = 32
    gaussian = True
    radius = 2
    border_size = 2

    removeTrees(editor)
    editor.flushBuffer()
    mapFeatures = MapFeatureExtractor(editor)
    visualize_map_features(mapFeatures, save=True)
    blueprint = Blueprint(mapFeatures)
    visualize_grid(blueprint, step_size=step_size, gaussian=gaussian, radius=radius, save=True)
    
    coordinator = AgentCoordinator(blueprint=blueprint, step_size=step_size, gaussian=gaussian, radius=radius)

    info = coordinator.generate(40, gaussian=gaussian, radius=radius, border_size=border_size)
    blueprint.show(save=True)
    blueprint.save_water_map()
    print(info)
    story_output_larger = generate_settlement_story(info)
    if "error" in story_output_larger:
        print("Error generating story:", story_output_larger["error"])
        if "raw_response" in story_output_larger:
            print("Raw response:", story_output_larger["raw_response"])
    else:
        for i, (id, rect) in enumerate(blueprint.house_locs.items()):
            story_output_larger["houses_and_families"][i]["location"] = rect

        print(story_output_larger)
        add_narrative(blueprint, story_output_larger)