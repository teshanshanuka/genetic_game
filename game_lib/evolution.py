__author__ = 'shash'

import numpy as np
import math
from random import randint
import random

def createNewPopulation(population, fitnessArray):
    # return new population
    pass

# parent pool selection stochastic universal sampling
def matingPool(population, fitnessArray, matingPoolPropotion):
    populationLength = len(population)
    matingPoolLength = math.floor(populationLength * matingPoolPropotion)

    distanceBetweenPointers = int(100 / matingPoolLength)
    startingPointer = randint(1, distanceBetweenPointers - 1)
    selectionPointers = []

    totalPopulationFitness = sum(fitnessArray)

    for i in range(0, matingPoolLength):
        nextPointer = int(startingPointer + i * distanceBetweenPointers)
        nextPointer = int(nextPointer * (totalPopulationFitness / 100))
        selectionPointers.append(nextPointer)

    unsortedFitnessArray = fitnessArray
    sortedFitnessArrayIndices = np.argsort(unsortedFitnessArray)
    fitnessArray.sort()
    y = np.cumsum(fitnessArray)

    selectedIndices = []

    for i in range(0, len(selectionPointers)):
        z = np.argmin(y < selectionPointers[i])
        selectedIndices.append(z)

    parentPool = []

    for i in range(0, len(selectedIndices)):
        correctIndex = sortedFitnessArrayIndices[selectedIndices[i]]
        parentPool.append(population[correctIndex])

    return parentPool


# cross over operations (one point cross over) for parent pool
def offspringPool(parentPool):
    crossOverPoint = randint(1, len(parentPool[0]) - 2)
    offSprings = []

    for i in range(0, math.floor(len(parentPool) / 2)):
        firstParent = parentPool[i]
        secondParent = parentPool[len(parentPool) - 1 - i]
        newOffspring1 = np.concatenate(
            (firstParent[0:crossOverPoint], secondParent[crossOverPoint: len(parentPool[0])]))
        newOffspring2 = np.concatenate(
            (secondParent[0:crossOverPoint], firstParent[crossOverPoint: len(parentPool[0])]))

        offSprings.append(newOffspring1)
        offSprings.append(newOffspring2)

    if len(parentPool) != len(offSprings):
        offSprings.append(parentPool[math.ceil(len(parentPool) / 2)])

    return offSprings


# mutate operations swap mutation
def mutatedPool(offSprings, mutationRate):
    for i in range(0, len(offSprings)):
        decider = random.uniform(0, 1)
        position1 = randint(0, len(offSprings[0]) - 1)
        position2 = randint(0, len(offSprings[0]) - 1)

        position1Value = offSprings[i][position1]
        position2Value = offSprings[i][position2]

        if decider < mutationRate:
            offSprings[i][position1] = position2Value
            offSprings[i][position2] = position1Value

    return offSprings


# next generation with elite individuals
def nextGeneration(population, offSprings, fitnessArray):
    sortedFitnessArrayIndices = np.argsort(fitnessArray)

    numbIndividualsToBeFilled = len(population) - len(offSprings)
    nextGenerationTemp = []

    for i in range(0, len(offSprings)):
        nextGenerationTemp.append(offSprings[i])

    for i in range(len(population) - numbIndividualsToBeFilled, len(population)):
        nextGenerationTemp.append(population[sortedFitnessArrayIndices[i]])

    return nextGenerationTemp


if __name__ == "__main__":
    init_genes = [np.random.uniform(low=0.2, high=1.0, size=(5,)) for _ in range(5)]
    fitness_arr = [np.random.randint(50,100) for _ in range(5)]

    new_pop = createNewPopulation(init_genes, fitness_arr)

    print("init genes:")
    for g in init_genes:
        print(g)

    print("\nnew pop:")
    for g in new_pop:
        print(g)