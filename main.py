# Fabricio J. C. Montenegro
# spl.splinter@gmail.com
# July 2017

import random
import copy
import time

# set of possible genes (chars)
geneSet = " qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM!,.;:<>?"
# the "dna" of the perfect individual
target = "Genetic Algorithms!"
# number of genes in the dna
NUM_GENES = len(target)

# NUM_GENERATIONS is only used if you test using it.
# The current code ends the program not based in the number of generations,
# but the fitness score of the fittest individual of the current generation
NUM_GENERATIONS = 10
# POP_SIZE is how many individuals you have in a generation
POP_SIZE = 500
# Truncation point, how many of the individuals will generate the new generation
SURVIVABILITY_RATE = 0.5
# Chance of a mutation happening in a generated individual
MUTATION_RATE = 0.1

# ultility function to find if a number is pair
pair = lambda x: True if x % 2 == 0 else False

# count is used to name individuals, each individual receives an id
count = 0

class Individual:
    def __init__(self):
        self.genes = []
        # generates a random list of genes from the set of possible genes with length = NUM_GENES
        for i in range(NUM_GENES):
            g = geneSet[random.randint(0,len(geneSet)-1)]
            self.genes.append(g)
        self.fitness = 0
        self.calc_fitness()
        global count
        self.id = count
        count += 1

    def calc_fitness(self):
        # evaluates the fitness of an individual by comparing it to the target
        score = 0
        for i, gene in enumerate(self.genes):
            if gene == target[i]:
                score += 1
        # the score is a percentual value (100 means it's equal to the target)
        percent = (score/float(NUM_GENES))*100.0
        self.fitness = percent
        return percent

    def sex(self, other):
        # when an individual is crossed with another to create a new one
        genes = []
        for i in range(NUM_GENES):
            # ran randomly determines which individual gives gene
            ran = random.randint(0,1)
            if pair(ran):
                genes.append(self.genes[i])
            else:
                genes.append(other.genes[i])
        # creates a new object
        ind = Individual()
        # and sets the selected genes to that new Individual
        ind.genes = list(genes)
        # updates the fitness of the new individual
        ind.calc_fitness()
        return ind

    def mutate(self):
        # a random gene is selected
        idx = random.randint(0, NUM_GENES-1)
        # and a random new gene is created
        new_gene = geneSet[random.randint(0,len(geneSet)-1)]
        # then we substitute the selected gene by the new one
        self.genes[idx] = new_gene
        self.calc_fitness()

    def get_string(self):
        # simply creates a string from the list of genes
        s = ''
        for g in self.genes:
            s += str(g)
        return s

    def __str__(self):
        # a pretty print showing ID, Genes, and Fitness
        return "["+ str(self.id) +"]Genes("+str(len(self.genes))+"):'" + self.get_string() + "' Fitness: " + str(self.fitness)

class Population:
    def __init__(self, old_pop=None):
        # if there's no older population
        if old_pop == None:
            # it's the first generation
            self.individuals = []
            # append POP_SIZE new individuals to the list of individuals
            for i in range(POP_SIZE):
                self.individuals.append(Individual())
        else:
            # next generations (selection)
            self.individuals = []
            # copy fittest individuals from last generation (survivors)
            # the number of survivors is given by num_survivors
            num_survivors = int(SURVIVABILITY_RATE * POP_SIZE)
            survivors = []
            for i in range(num_survivors):
                survivors.append(copy.deepcopy(old_pop.individuals[i]))

            # after the survivors are selected, they are crossed to create new individuals
            self.crossover(survivors)
        # and sort them by fitness (fittest first)
        self.individuals.sort(key=lambda i: i.fitness, reverse=True)


    def crossover(self, survivors):
        # detect number of survivors
        num_survivors = len(survivors)
        # we're gonna save the strings generated to make sure we are not generating repeated strings
        strings = []
        # we need POP_SIZE new individuals
        while len(self.individuals) < POP_SIZE:
            different = False
            # while the new individual is not different from the others
            while not different:
                # select two random individuals from the survivors to cross
                ind1 = survivors[random.randint(0,num_survivors-1)]
                ind2 = survivors[random.randint(0,num_survivors-1)]
                # and a new individual is created
                new_individual = ind1.sex(ind2)

                # detects if a mutation should occur in the created individual
                if random.random() < MUTATION_RATE:
                    new_individual.mutate()

                # if there's no one with the same string as this new individual in the string
                if not new_individual.get_string() in strings:
                    # it means he is different
                    different = True
                    # and we can add it to the list
                    self.individuals.append(new_individual)
                    strings.append(new_individual.get_string())
                
    def avg_fitness(self):
        # self explanatory?
        avg = 0
        for ind in self.individuals:
            avg += ind.fitness
        return avg/float(len(self.individuals))

    def get_fittest(self):
        # as the list of individuals is always ordered by fitness, the first one is the fittest one
        return self.individuals[0]

    def __str__(self):
        # pretty print shows the individuals of this population
        s = ""
        for i in self.individuals:
            s += str(i) + '\n'
        # and the average fitness
        s += "avg fitness: " + str(self.avg_fitness())
        return s

# # IF YOU WANT TO LIMIT YOUR TEST BY THE NUMBER OF GENERATIONS
# generations = []
# for i in range(NUM_GENERATIONS):
#     print "GENERATION " + str(i) + ":"
#     if len(generations) == 0:
#         generations.append(Population())
#     else:
#         last_generation = generations[-1]
#         generations.append(Population(last_generation))
#     print generations[-1]
#     print "Generation", i, "Avg Fitness:", generations[-1].avg_fitness(), "Fittest: ", generations[-1].individuals[0].get_string(), "with fitness", generations[-1].individuals[0].fitness
#     time.sleep(0.2)

# TESTING UNTIL WE GET THE TARGET INDIVIDUAL
# max fitness starts at zero and goes up
max_fitness = 0
generation_count = 0

print "Target: '{0}', Population size: {1}".format(target, POP_SIZE)
print "Chance of mutation: {0}, Survivability rate: {1}".format(MUTATION_RATE, SURVIVABILITY_RATE)

while max_fitness < 100:
    if generation_count == 0:
        # if this is the first generation, just create a random population
        generation = Population()
    else:
        # otherwise, we save the last generation
        last_generation = copy.deepcopy(generation)
        # and use it to create a new one
        generation = Population(last_generation)

    # if the fittest individual has a higher fitness score than the max so far
    if generation.individuals[0].fitness > max_fitness:
        # sets the new max fitness
        max_fitness = generation.individuals[0].fitness

    generation_count += 1

    # this print will show:
    # the generation count, the average fitness, the fittest individual from that generation, and its fitness
    print "{0:03d}({1:.2f}): Fittest: '{2}' with fitness {3:.2f}".format(generation_count, generation.avg_fitness(), generation.individuals[0].get_string(), generation.individuals[0].calc_fitness())

    time.sleep(0.2)
