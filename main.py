import json
import random
from typing import NamedTuple, List, Tuple
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Coordinate(NamedTuple):
    x: float
    y: float
    z: float


class Resource(NamedTuple):
    name: str
    weight: float
    value: float


class Planet(NamedTuple):
    name: str
    coord: Coordinate
    resources: List[Resource]


class Spaceship:
    max_weight: float
    current_weight: float
    current_value: float
    resources: List[Resource]
    base: Coordinate

    def __init__(self, max_weight: float, base: Coordinate = Coordinate(0, 0, 0)):
        self.max_weight = max_weight
        self.current_weight = 0
        self.current_value = 0
        self.resources = []
        self.base = base

    def __str__(self):
        resource_names = [resource.name for resource in self.resources]
        return (f"Value=[{self.current_value}] - Weight=[{self.current_weight}/{self.max_weight}] - Resources={resource_names}")

    def load_resources(self, resources: List[Resource]) -> bool:
        sorted_resources = sorted(resources, key=lambda r: r.value / r.weight, reverse=True)
        for resource in sorted_resources:
            remaining_weight = self.max_weight - self.current_weight
            if remaining_weight <= 0:
                return False
            if resource.weight <= remaining_weight:
                self.resources.append(resource)
                self.current_weight += resource.weight
                self.current_value += resource.value
            else:
                fraction = remaining_weight / resource.weight
                partial_weight = resource.weight * fraction
                partial_value = resource.value * fraction
                partial_resource = Resource(name=resource.name, weight=partial_weight, value=partial_value)
                self.resources.append(partial_resource)
                self.current_weight += partial_resource.weight
                self.current_value += partial_resource.value
                return True
        return True

    def _calculate_distance(self, coord1: Coordinate, coord2: Coordinate) -> float:
        return math.sqrt(
            (coord1.x - coord2.x) ** 2 +
            (coord1.y - coord2.y) ** 2 +
            (coord1.z - coord2.z) ** 2
        )

    def _simulate_path_value(self, planets: List[Planet]) -> float:
        temp_weight = 0
        temp_value = 0
        for planet in planets:
            sorted_resources = sorted(planet.resources, key=lambda r: r.value / r.weight, reverse=True)
            for resource in sorted_resources:
                remaining_weight = self.max_weight - temp_weight
                if remaining_weight <= 0:
                    break
                if resource.weight <= remaining_weight:
                    temp_weight += resource.weight
                    temp_value += resource.value
                else:
                    fraction = remaining_weight / resource.weight
                    temp_weight += resource.weight * fraction
                    temp_value += resource.value * fraction
                    break
        return temp_value

    def analyze_path(self, planets: List[Planet]) -> Tuple[Planet, ...]:
        if not planets:
            return tuple()
        best_path = []
        best_value = 0
        for start_planet in planets:
            unvisited = [p for p in planets if p != start_planet]
            current_path = [start_planet]
            current_position = self.base
            current_position = start_planet.coord
            while unvisited:
                best_next = None
                best_score = -1
                for planet in unvisited:
                    distance = self._calculate_distance(current_position, planet.coord)
                    planet_value = sum(r.value for r in planet.resources)
                    score = planet_value / distance if distance > 0 else planet_value
                    if score > best_score:
                        best_score = score
                        best_next = planet
                current_path.append(best_next)
                unvisited.remove(best_next)
                current_position = best_next.coord
            path_value = self._simulate_path_value(current_path)
            if path_value > best_value:
                best_value = path_value
                best_path = current_path
        self.current_weight = 0
        self.current_value = 0
        self.resources = []
        for planet in best_path:
            self.load_resources(planet.resources)
        return tuple(best_path)


def load_planets_from_json(filename: str) -> List[Planet]:
    with open(filename, 'r') as f:
        data = json.load(f)
    planets = []
    for p in data:
        coord = Coordinate(**p['coord'])
        resources = [Resource(**r) for r in p['resources']]
        planets.append(Planet(name=p['name'], coord=coord, resources=resources))
    return planets

def plot_spaceship_route_3d(spaceship: Spaceship, route: Tuple[Planet, ...], title="Optimal Spaceship Route 3D"):
    if not route:
        print("No route to plot")
        return
    
    x = [planet.coord.x for planet in route]
    y = [planet.coord.y for planet in route]
    z = [planet.coord.z for planet in route]
    
    x = [spaceship.base.x] + x + [spaceship.base.x]
    y = [spaceship.base.y] + y + [spaceship.base.y]
    z = [spaceship.base.z] + z + [spaceship.base.z]
    
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot(x, y, z, marker='o', linestyle='-', color='blue', linewidth=2, markersize=8)
    
    ax.scatter(spaceship.base.x, spaceship.base.y, spaceship.base.z, color='red', marker='s', s=100, label='Base')
    
    for i, planet in enumerate(route):
        ax.text(planet.coord.x, planet.coord.y, planet.coord.z + 0.5, 
                f'{i+1}. {planet.name}', 
                fontsize=9, ha='center', va='bottom',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))
    
    ax.text(spaceship.base.x, spaceship.base.y, spaceship.base.z - 0.8, 'BASE', 
            fontsize=10, ha='center', va='top', weight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='red', alpha=0.7, edgecolor='darkred'))
    
    min_x, max_x = ax.get_xlim()
    min_y, max_y = ax.get_ylim()
    min_z, max_z = ax.get_zlim()
    
    text_x = (max_x + min_x) / 2
    text_y = (max_y + min_y) / 2
    text_z = min_z - (max_z - min_z) * 0.1
    
    status_text = (f'Total Value: {spaceship.current_value:.1f}\n'
                  f'Weight: {spaceship.current_weight:.1f}/{spaceship.max_weight}\n'
                  f'Resources: {len(spaceship.resources)}')
    
    ax.text(text_x, text_y, text_z, status_text, 
            fontsize=12, color='darkgreen', weight='bold',
            bbox=dict(facecolor='lightyellow', alpha=0.9, edgecolor='darkgreen', linewidth=2),
            ha='center', va='top')
    
    ax.set_title(title, fontsize=14, weight='bold')
    ax.set_xlabel("X Coordinate", fontsize=12)
    ax.set_ylabel("Y Coordinate", fontsize=12)
    ax.set_zlabel("Z Coordinate", fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    all_planets = load_planets_from_json('planets.json')
    N = random.randint(5, 50)
    N = min(N, len(all_planets))
    selected_planets = random.sample(all_planets, N)
    ship = Spaceship(max_weight=150)
    optimal_path = ship.analyze_path(selected_planets)
    print(f"Number of planets to visit: {N}")
    print("Visit order for maximum value:")
    for i, planet in enumerate(optimal_path, 1):
        print(f"{i}. {planet.name}")
    print(f"\nFinal spaceship status: {ship}")

    plot_spaceship_route_3d(spaceship=ship, route=optimal_path)
