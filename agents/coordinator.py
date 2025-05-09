from Error import CustomError
from maps.blueprint import Blueprint
from .roadAgent import RoadConnectorAgent
from .housingAgent import HousingAgent
from .churchAgent import ChurchAgent
from .farmAgent import FarmAgent
from .StructuralAgent import StructuralAgent
import numpy as np


class AgentCoordinator:
    def __init__(self, blueprint: Blueprint, step_size = 32):

        self.blueprint = blueprint

        _, begin = self.blueprint.get_town_center(step_size=step_size)
        end = [begin[0] + step_size - 1, begin[1] + step_size - 1]
        self.min_coords = begin
        self.max_coords = end

        self.timestep = 0
        self.active_agents: list[StructuralAgent] = []

        self.road_connector_agent = RoadConnectorAgent(blueprint=blueprint)

        self.housing_agent = HousingAgent(blueprint=blueprint, 
                                          search_area=[self.min_coords, self.max_coords], 
                                          road_connector_agent=self.road_connector_agent, 
                                          activation_step=0,
                                          priority=0,
                                          max_slope=1,
                                          min_width=8, 
                                          min_height=8, 
                                          max_width=14, 
                                          max_height=14,
                                          max_plots=100)
        
        self.farm_agent = FarmAgent(blueprint=blueprint, 
                                    search_area=[self.min_coords, self.max_coords], 
                                    road_connector_agent=self.road_connector_agent,
                                    activation_step=25,
                                    priority=1,
                                    max_slope=1,
                                    min_width=6, 
                                    min_height=6, 
                                    max_width=15, 
                                    max_height=15,
                                    max_plots=5)
        self.church_agent = ChurchAgent(blueprint=blueprint, 
                                        search_area=[self.min_coords, self.max_coords], 
                                        road_connector_agent=self.road_connector_agent,
                                        activation_step=0,
                                        priority=2,
                                        max_slope=1,
                                        min_width=17, 
                                        min_height=17, 
                                        max_width=25, 
                                        max_height=25,
                                        max_plots=1)

        self.road_connector_agent.place([[begin[0]  + step_size // 2, begin[1] + step_size // 2]])

    def _update_active_agents(self):
        self.active_agents.clear()
        for agent in [self.housing_agent, self.farm_agent, self.church_agent]:
            if agent.activation_step <= self.timestep and agent.plots_left != 0:
                self.active_agents.append(agent)


    def step(self, execute=True):
        self.timestep += 1
        self._update_active_agents()
        if len(self.active_agents) == 0:
            print("No active agent")
            return

        chosen_agent = None
        for agent in sorted(
                self.active_agents, 
                key=lambda x: x.priority,
                reverse=True
            ):
            try:
                agent.choose(expansion=32)
            except IndexError as e:
                print(e)
                continue
            if agent.current_choice != None:
                chosen_agent = agent
                print(f"Agent of type {agent.type.name} activated!")
                break
        
        if chosen_agent != None:

            chosen_agent.place()

            if execute:
                w, h = [chosen_agent.current_choice[0][-1][0] - chosen_agent.current_choice[0][0][0] + 1, chosen_agent.current_choice[0][-1][1] - chosen_agent.current_choice[0][0][1] + 1]
                chosen_agent.terrain_manipulator.place_base(chosen_agent.current_choice[0][0], w, h)

            chosen_agent.road_connector_agent.connect_to_road_network(chosen_agent.current_choice[1], execute)
        else:
            raise NoneTypeAgent("No agent available")

    def generate(self, steps):
        for i in range(steps):
            try:
                self.step()
            except IndexError as e:
                print(e)
                break
            except NoneTypeAgent as e:
                print(e)
            except CustomError as e:
                print(e)
            print(f"Timestep: {self.timestep}")
            
    
    
    
class NoneTypeAgent(Exception):
    pass