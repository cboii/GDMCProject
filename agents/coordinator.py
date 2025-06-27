from matplotlib import pyplot as plt
from Error import CustomError
from .townHallAgent import TownHallAgent
from .cityWallAgent import CityWallAgent
from maps.blueprint import Blueprint
from .roadAgent import RoadConnectorAgent
from .housingAgent import HousingAgent
from .churchAgent import ChurchAgent
from .farmAgent import FarmAgent
from .innAgent import InnAgent
from .decorationAgent import DecorationAgent
from .StructuralAgent import NoValidPath, NoneTypeChoice, StructuralAgent
from .wellAgent import WellAgent
from .miscAgent import MiscAgent
import random


class AgentCoordinator:
    def __init__(self, blueprint: Blueprint, step_size = 32, gaussian=False, radius=1):

        self.blueprint = blueprint

        _, begin = self.blueprint.get_town_center(step_size=step_size, gaussian=gaussian, radius=radius)
        end = [begin[0] + step_size - 1, begin[1] + step_size - 1]
        self.min_coords = begin
        self.max_coords = end

        self.timestep = 0
        self.active_agents: list[StructuralAgent] = []

        self.road_connector_agent = RoadConnectorAgent(blueprint=blueprint, 
                                                       max_width=3, 
                                                       max_slope=1)
        border_size = 2

        self.housing_agent = HousingAgent(blueprint=blueprint, 
                                          road_connector_agent=self.road_connector_agent, 
                                          activation_step=0,
                                          priority=1,
                                          max_slope=2,
                                          max_plots=100,
                                          outside_walls=False,
                                          border=border_size,
                                          sizes = list(set([(h, w)
                                            for h in range(11, 17 + 1)
                                            for w in range(11,  20 + 1)]) | 
                                            set([(h, w)
                                            for h in range(11,  20 + 1)
                                            for w in range(11, 17 + 1)])))
        
        self.town_hall_agent = TownHallAgent(blueprint=blueprint, 
                                          road_connector_agent=self.road_connector_agent, 
                                          activation_step=0,
                                          priority=3,
                                          max_slope=2,
                                          max_plots=1,
                                          outside_walls=False,
                                          inside_walls=True,
                                          border=border_size,
                                          sizes = [(22, 21), (28, 22), (21, 22), (22, 28)])
        
        self.farm_agent = FarmAgent(blueprint=blueprint,  
                                    road_connector_agent=self.road_connector_agent,
                                    activation_step=8,
                                    priority=2,
                                    max_slope=2,
                                    max_plots=5,
                                    outside_walls=True,
                                    border=border_size,
                                    sizes= [(h, w)
                                            for h in range(17, 26 + 1)
                                            for w in range(17,  26 + 1)])
        self.church_agent = ChurchAgent(blueprint=blueprint,
                                        road_connector_agent=self.road_connector_agent,
                                        activation_step=0,
                                        priority=3,
                                        max_slope=2,
                                        max_plots=1,
                                        outside_walls=False,
                                        inside_walls=True,
                                        border=border_size,
                                        sizes=[(21, 13), (28, 13), (13, 21), (13, 28)])
        self.city_wall_agent = CityWallAgent(blueprint=blueprint,
                                        activation_step=11,
                                        priority=3,
                                        max_slope=5,
                                        max_plots=1,
                                        road_connector_agent=self.road_connector_agent,
                                        number_of_gates=3)
        self.inn_agent = InnAgent(blueprint=blueprint,
                                        road_connector_agent=self.road_connector_agent,
                                        activation_step=0,
                                        priority=2,
                                        max_slope=2,
                                        max_plots=1,
                                        outside_walls=False,
                                        border=border_size,
                                        sizes=[(15, 13), (20, 13), (25, 13), (13, 15), (13, 20), (13, 25)])
        self.decoration_agent = DecorationAgent(blueprint=blueprint,
                                        road_connector_agent=self.road_connector_agent,
                                        activation_step=10,
                                        priority=-1,
                                        max_slope=2,
                                        max_plots=100,
                                        outside_walls=False,
                                        inside_walls=True,
                                        border=border_size,
                                        sizes=[(5,4), (4,5)],
                                        road_connection=False)
        self.well_agent = WellAgent(blueprint=blueprint,
                                        road_connector_agent=self.road_connector_agent,
                                        activation_step=10,
                                        priority=0,
                                        max_slope=2,
                                        max_plots=2,
                                        outside_walls=False,
                                        border=border_size,
                                        sizes=[(7,7)])
        self.misc_agent = MiscAgent(blueprint=blueprint,
                                        road_connector_agent=self.road_connector_agent,
                                        activation_step=5,
                                        priority=1,
                                        max_slope=2,
                                        max_plots=1,
                                        outside_walls=False,
                                        border=border_size,
                                        sizes=[(12,9),(9,12)])

        self.road_connector_agent.place([[begin[0]  + step_size // 2, begin[1] + step_size // 2]])

    def _update_active_agents(self):
        self.active_agents.clear()
        agents = [self.housing_agent, self.farm_agent, self.church_agent, self.town_hall_agent, self.inn_agent, self.decoration_agent, self.well_agent, self.misc_agent]
        random.shuffle(agents)
        for agent in agents:
            if agent.activation_step <= self.timestep and agent.plots_left != 0:
                self.active_agents.append(agent)


    def expand_search_area(self, expansion):
        expansion = expansion

        expansion_left = expansion
        expansion_right = expansion
        expansion_top = expansion
        expansion_bottom = expansion

        if (self.min_coords[0] - expansion < 0 and self.min_coords[1] - expansion < 0) and (self.max_coords[0] + expansion > (self.blueprint.map.shape[0] - 1) and self.max_coords[1] + expansion > (self.blueprint.map.shape[1] - 1)):
            print(f"--- Borders reached ---")
            expansion_top = 0
            expansion_bottom = 0
            expansion_left = 0
            expansion_right = 0
        
        if self.max_coords[1] + expansion > (self.blueprint.map.shape[1] - 1):
            expansion_top = 0
        
        if self.min_coords[1] - expansion < 0:
            expansion_bottom = 0

        if self.min_coords[0] - expansion < 0:
            expansion_left = 0

        if self.max_coords[0] + expansion > (self.blueprint.map.shape[0] - 1):
            expansion_right = 0

        self.min_coords = [self.min_coords[0] - expansion_left, self.min_coords[1] - expansion_bottom]
        self.max_coords = [self.max_coords[0] + expansion_right, self.max_coords[1] + expansion_top]

    
    def step(self, expansion=16, execute=True, gaussian=False, radius=1, border_size=3, walls_placed=False):
        self.timestep += 1
        self._update_active_agents()
        if len(self.active_agents) == 0:
            print("--- No active agent ---")
            return

        chosen_agent = None
        for agent in sorted(
                self.active_agents, 
                key=lambda x: x.priority,
                reverse=True
            ):
            try:
                agent.choose(search_area=(self.min_coords, self.max_coords), gaussian=gaussian, radius=radius, border_size=border_size, walls_placed=walls_placed)
            # except IndexError as e:
            #     print(e)
            #     continue
            except NoneTypeChoice as e:
                print(e)
                continue
            except NoValidPath as e:
                print(e)
                continue
            if agent.current_choice != None:
                chosen_agent = agent
                print(f"--- Agent of type {agent.type.name} activated! ---")
                break
        
        if chosen_agent != None:            
            chosen_agent.place()

            if execute:
                w, h = [chosen_agent.current_choice[0][-1][0] - chosen_agent.current_choice[0][0][0] + 1, chosen_agent.current_choice[0][-1][1] - chosen_agent.current_choice[0][0][1] + 1]
                chosen_agent.terrain_manipulator.place_base(chosen_agent.current_choice[0][0], w, h)

            if chosen_agent.road_connection:
                chosen_agent.road_connector_agent.connect_to_road_network([tuple(x) for x in chosen_agent.current_path], execute)

            if execute:
                chosen_agent.build([chosen_agent.current_choice[0][0][0], chosen_agent.current_choice[0][0][1]], w, h)
                self.blueprint.map_features.editor.flushBuffer()
                self.blueprint.reload_feature_maps()
            

        else:
            self.expand_search_area(expansion)
            raise NoneTypeAgent("--- No agent available! ---")
        self.blueprint.map_features.editor.flushBuffer()

    def generate(self, steps, gaussian=False, radius=1, border_size=3):
        
        city_walls_placed = False
        walls_placed = False
        for i in range(steps):
            if i >= steps * 1/2 and city_walls_placed == False:
                success = self.city_wall_agent.try_place()
                if success:
                    
                    print("--- City walls placed! ---")
                    city_walls_placed = True
                    walls_placed = True
                    continue
            try:
                self.step(gaussian=gaussian, radius=radius, border_size=border_size, walls_placed=walls_placed)
            # except IndexError as e:
            #     print(e)
            #     break
            except NoneTypeAgent as e:
                print(e)
            except CustomError as e:
                print(e)
            print(f"--- Timestep: {self.timestep} ---")
            walls_placed = False
        self.city_wall_agent.execute_wall_placement()

        self.blueprint.map_features.editor.flushBuffer()
        info = {"data": {}}
        for agent in [self.housing_agent, self.farm_agent, self.church_agent, self.town_hall_agent, self.inn_agent, self.decoration_agent, self.well_agent, self.misc_agent]:
            info["data"][agent.type.name] = {
                "number_of_plots": agent.max_plots - agent.plots_left
                }
        info["blueprint"] = self.blueprint.map
        info["water_map"] = self.blueprint.ground_water_map
        info["biome"] = self.blueprint.map_features.editor.getBiome((int(self.blueprint.ground_water_map.shape[0]/2), self.blueprint.height_map[int(self.blueprint.ground_water_map.shape[0]/2), int(self.blueprint.ground_water_map.shape[1]/2)], int(self.blueprint.ground_water_map.shape[1]/2)))

        return info    
class NoneTypeAgent(Exception):
    pass