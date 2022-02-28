import random

def nearest_neighbour_solution():
    curr_node = 0
    visited = set([])
    solution = []
    solution.append(curr_node)
    visited.add(curr_node)
    solution_fitness = 0
    while len(solution) < n:
        neighbour_distances = [(distances[(curr_node, i)], i) for i in range(n) if i not in visited]
        min_dist, min_neighbour = min(neighbour_distances)
        curr_node = min_neighbour
        solution_fitness += min_dist
        solution.append(curr_node)
        visited.add(curr_node)
    fitness_dict[tuple(solution)] = solution_fitness
    return solution

def initialize_distances():
    for i in range(n):
        distances[(i, i)] = 0
        for j in range(i + 1, n):
            distance = random.uniform(500, 1500)
            distances[(i, j)] = distance
            distances[(j, i)] = distance
    return

def initiate(n):
    initial_population = []
    approximated_solution = nearest_neighbour_solution()
    initial_population.append(tuple(approximated_solution))
    for i in range(len(approximated_solution)):
        for j in range(i + 1, len(approximated_solution)):
            approximated_solution[i], approximated_solution[j] = approximated_solution[j], approximated_solution[i]
            initial_population.append(tuple(approximated_solution))
            approximated_solution[i], approximated_solution[j] = approximated_solution[j], approximated_solution[i]
    while len(initial_population) < n ** 2:
        permutation = tuple(random.sample(list(range(n)), n))
        initial_population.append(permutation)
    return initial_population


def fitness_function(distances, city_permutation, fitness_dict):
    if city_permutation in fitness_dict:
        return fitness_dict[city_permutation]
    total_distance = 0
    for i in range(len(city_permutation) - 1):
        total_distance += distances[(city_permutation[i], city_permutation[i + 1])]
    total_distance += distances[(city_permutation[len(city_permutation) - 1], city_permutation[0])]
    fitness_dict[city_permutation] = total_distance
    return total_distance


def tournament_selection(population, fitness_dict, m):
    random_sample = random.sample(list(range(len(population))), m)
    tournament_list = [(fitness_dict[population[sample]], population[sample]) for sample in random_sample]
    return min(tournament_list)[1]


def roulette_wheel_selection(population, fitness_dict):
    total_sum = 0
    for chromozome in population:
        total_sum += fitness_function(distances, chromozome, fitness_dict)
    choice = random.uniform(0, total_sum)
    current = 0
    for chromozome in population:
        current += fitness_dict[chromozome]
        if current > choice:
            return chromozome


def find_cycles(permutation1, permutation2):
    visited = set([])
    cycles = []
    for el in range(len(permutation1)):
        if el not in visited:
            curr_cycle = []
            start_el = permutation1[el]
            curr_cycle.append(el)
            pos = permutation1.index(permutation2[el])
            visited.add(el)
            while permutation2[pos] != start_el:
                curr_cycle.append(pos)
                pos = permutation1.index(permutation2[pos])
                visited.add(pos)
            if pos not in curr_cycle:
                curr_cycle.append(pos)
            for idx in curr_cycle:
                if idx not in visited:
                    visited.add(idx)
            cycles.append(curr_cycle)

    return cycles

def cycle_crossover(parent1, parent2, n):
    cycles = find_cycles(parent1, parent2)
    child1, child2 = [0] * n, [0] * n
    for idx in range(len(cycles)):

        cycle = cycles[idx]
        for el in cycle:

            if idx % 2 == 0:
                child1[el] = parent1[el]
                child2[el] = parent2[el]
            else:
                child1[el] = parent2[el]
                child2[el] = parent1[el]

    return tuple(child1), tuple(child2)


def order_one_crossover(parent1, parent2):
    childP1 = []

    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])

    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return tuple(child)

def mutation(chromozome, pm=0.015):
    chromozome = list(chromozome)
    for i in range(len(chromozome)):
        rand = random.uniform(0, 1)
        if rand <= pm:
            idx = random.randint(0, len(chromozome) - 1)
            chromozome[i], chromozome[idx] = chromozome[idx], chromozome[i]
    chromozome = tuple(chromozome)


def generation_change(previous_generation, new_generation, m):
    previous_generation.sort(key=lambda x: fitness_function(distances, x, fitness_dict))
    new_generation.sort(key=lambda x: fitness_function(distances, x, fitness_dict))
    result = []
    result += previous_generation[0:m:1]
    result += new_generation[0:n - m:1]
    return result

def genetic_algorithm(n):
    initial_population = initiate(n)
    selection_size = int(n / 4)
    solutionFound = False
    solution = min(initial_population, key=lambda x: fitness_function(distances, x, fitness_dict))
    counter = 0
    iter_counter = 0

    while not solutionFound and iter_counter < 1000:

        selection_pool = []
        new_generation = []
        while len(selection_pool) < selection_size:
            new_chromozome = roulette_wheel_selection(initial_population, fitness_dict)
            selection_pool.append(new_chromozome)

        for i in range(len(selection_pool)):
            for j in range(i + 1, len(selection_pool)):
                chromozome1, chromozome2 = selection_pool[i], selection_pool[j]
                child1,child2 = cycle_crossover(chromozome1, chromozome2,n)
                new_generation.append(child1)
                new_generation.append(child2)

        for chromozome in new_generation:
            mutation(chromozome, 0.02)

        initial_population = generation_change(initial_population, new_generation, int(3 * n / 4))
        new_solution = min(initial_population, key=lambda x: fitness_function(distances, x, fitness_dict))

        if new_solution < solution:
            counter = 0
            solution = new_solution

        else:
            if counter == 3:
                solutionFound = True
            else:
                counter += 1

        iter_counter += 1

    return solution

n = int(input("Unesite broj gradova "))
s=0
for i in range (30):
    distances = {}
    fitness_dict = {}
    initialize_distances()
    solution = genetic_algorithm(n)
    f=(fitness_function(distances, solution, fitness_dict))
    s+=f

print(s/30)