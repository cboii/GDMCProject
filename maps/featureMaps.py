from gdpc import Editor, block
from gdpc.vector_tools import Vec3iLike
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

class MapFeatureExtractor:
    def __init__(self, editor: Editor):
        self.editor = editor
        self.build_area = editor.getBuildArea()
        self.world_slice = editor.loadWorldSlice()
    
    def _get_dimensions(self, first: Vec3iLike , last: Vec3iLike):
        if first == None:
            first = (0,0,0)
        
        if last == None: 
            last = self.build_area.end-self.build_area.offset
        
        length = last[0] - first[0]
        width = last[2] - first[2]
        return first, last, length, width

    def create_biome_map(self, first: Vec3iLike = None, last: Vec3iLike = None):
        first, last, length, width = self._get_dimensions(first,last)

        map = np.empty((length,width), dtype=object)

        for x in range(0,length):
            for z in range(0,width):
                map[x,z] = self.world_slice.getBiome((first[0]+x,100,first[2]+z))
        
        return map

    def create_groundwater_map(self, first: Vec3iLike = None, last: Vec3iLike = None):
        first, last, length, width = self._get_dimensions(first, last)
        heightmap = self.world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

        map = np.full((length,width), fill_value=16)
        
        for x in range(0,length):
            for z in range(0,width):
                for i in range(0,8):
                    if self.world_slice.getBlock((first[0]+x, heightmap[first[0]+x, first[2]+z]-1-i, first[2]+z)).id == "minecraft:water":
                        map[x,z] = i
                        break
                    else:
                        # Set anything else to 255
                        map[x,z] = 255
        
        return map
        
    def create_gradient_maps(self,  first: Vec3iLike = None, last: Vec3iLike = None):
        first, last, length, width = self._get_dimensions(first, last)
        heightmap = self.world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
        map_posX = np.zeros((length,width))
        map_negX = np.zeros((length,width))
        map_posZ = np.zeros((length,width))
        map_negZ = np.zeros((length,width))
        map_sum = np.zeros((length,width))

        for x in range(0,length-1):
            for z in range(0,width):
                map_posX[x,z] = heightmap[x+1,z]-heightmap[x,z]
                map_sum[x,z] = map_posX[x,z]**2
        
        for x in range(1,length):
            for z in range(0,width):
                map_negX[x,z] = heightmap[x-1,z]-heightmap[x,z]
        
        for z in range(0,width-1):
            for x in range(0,length):
                map_posZ[x,z] = heightmap[x,z+1]-heightmap[x,z]
                map_sum[x,z] += map_posZ[x,z]**2
        
        for z in range(1,width):
            for x in range(0,length):
                map_negZ[x,z] = heightmap[x,z-1]-heightmap[x,z]


        return map_posX, map_negX, map_posZ, map_negZ, np.sqrt(map_sum)
    
    def create_heightmap(self):
        return self.world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    