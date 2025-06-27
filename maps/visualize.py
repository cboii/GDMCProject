from .featureMaps import MapFeatureExtractor
from .blueprint import Blueprint
import numpy as np
import matplotlib.pyplot as plt
from skimage import data, segmentation, color
from skimage import graph

def visualize_map_features(map_features: MapFeatureExtractor):
    f, axes = plt.subplots(1, 3)
    axes[0].imshow(np.rot90(map_features.create_heightmap()), cmap='magma', interpolation='nearest', origin='lower')
    axes[0].set_title('Height Map')
    axes[1].imshow(np.rot90(map_features.create_gradient_maps()[4]), cmap='viridis', interpolation='nearest', origin='lower')
    axes[1].set_title('Steepness Map')
    axes[2].imshow(np.rot90(map_features.create_groundwater_map()), cmap='magma', interpolation='nearest', origin='lower')
    axes[2].set_title('Ground Water Map')

    plt.show()

def visualize_grid(map: Blueprint, step_size, gaussian=False, radius=1):
    f, axes = plt.subplots(1,3)
    area = map.get_buildable_area(step_size=2, gaussian=gaussian, radius=radius)
    town_center = map.get_town_center(step_size=step_size, gaussian=gaussian, radius=radius)
    _, _, _, _, subregion = map.get_subregion(town_center[1], region_size=step_size, gaussian=gaussian, radius=radius)
    axes[0].imshow(np.rot90(area), cmap='magma', interpolation='nearest', origin='lower')
    axes[0].set_title('Grid')
    axes[1].imshow(np.rot90(town_center[0]), cmap='magma', interpolation='nearest', origin='lower')
    axes[1].set_title('Town Center')
    axes[2].imshow(np.rot90(subregion), cmap='magma', interpolation='nearest', origin='lower')
    axes[2].set_title('Town Center Region')

    plt.show()