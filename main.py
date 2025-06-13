import json
import random
from typing import NamedTuple, List, Tuple
import math


class Coordinates(NamedTuple):
    x: float
    y: float
    z: float


class Resource(NamedTuple):
    name: str
    weight: float
    value: float


class Planet(NamedTuple):
    name: str
    coord: Coordinates
    resources: List[Resource]


class Spaceship:
    max_weight: float
    current_weight: float
    current_value: float
    resources: List[Resource]
    base: Coordinates

    def __init__(self, max_weight: float, base: Coordinates = Coordinates(0, 0, 0)):
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

    def _calculate_distance(self, coord1: Coordinates, coord2: Coordinates) -> float:
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
        coord = Coordinates(**p['coord'])
        resources = [Resource(**r) for r in p['resources']]
        planets.append(Planet(name=p['name'], coord=coord, resources=resources))
    return planets

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
