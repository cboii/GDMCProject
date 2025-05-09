from .StructuralAgent import StructuralAgent
from .plots import PlotType

class FarmAgent(StructuralAgent):

    def __init__(self, 
                 blueprint, 
                 search_area, 
                 road_connector_agent, 
                 activation_step, priority, 
                 max_slope,
                 min_width, 
                 min_height, 
                 max_width, 
                 max_height,
                 max_plots):
        super().__init__(blueprint, 
                         search_area, 
                         road_connector_agent, 
                         activation_step, 
                         priority, 
                         max_slope,
                         min_width, 
                         min_height, 
                         max_width, 
                         max_height,
                         max_plots)
        
        self.max_distance_to_road = 10
        self.max_slope = max_slope
        self.type = PlotType.FARM

        self.min_width=min_width
        self.min_height=min_height
        self.max_width=max_width
        self.max_height=max_height
