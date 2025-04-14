from .featureMaps import MapFeatureExtractor
from .buildMaps import BuildMap
import numpy as np
import matplotlib.pyplot as plt

def visualize_map_features(map_features: MapFeatureExtractor):
    f, axes = plt.subplots(1, 3)
    axes[0].imshow(map_features.create_heightmap(), cmap='magma', interpolation='nearest', origin='lower')
    axes[0].set_title('Height Map')
    axes[1].imshow(map_features.create_gradient_maps()[4], cmap='viridis', interpolation='nearest', origin='lower')
    axes[1].set_title('Steepness Map')
    axes[2].imshow(map_features.create_groundwater_map(), cmap='magma', interpolation='nearest', origin='lower')
    axes[2].set_title('Ground Water Map')

    plt.show()

def visualize_grid(map: BuildMap, step_size, gaussian=False):
    f, axes = plt.subplots(1,3)
    area = map.get_buildable_area(step_size=2, gaussian=True)
    town_center = map.get_town_center(gaussian=gaussian, step_size=step_size)
    subregion = map.get_subregion(town_center[1], region_size=step_size)
    axes[0].imshow(area, cmap='magma', interpolation='nearest', origin='lower')
    axes[0].set_title('Grid')
    axes[1].imshow(town_center[0], cmap='magma', interpolation='nearest', origin='lower')
    axes[1].set_title('Town Center District Location')
    axes[2].imshow(subregion, cmap='magma', interpolation='nearest', origin='lower')
    axes[2].set_title('Town Center District')

    plt.show()