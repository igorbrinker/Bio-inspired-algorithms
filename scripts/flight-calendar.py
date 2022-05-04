import time
import random
import math
import sys

#DATA TREATMENT ALGORITHM

#loading people`s first location
passenger = [('Lisbon', 'LIS'),
            ('Madrid', 'MAD'),
            ('Paris', 'CDG'),
            ('Dublin', 'DUB'),
            ('Brussels', 'BRU'),
            ('London', 'LHR')]

#rome airport
destination = 'FCO'

flights = {}

for line in open('../data/flights.txt'):
  # print(line)
  origin, destination, departure, arrival, price = line.split(',')
  print(origin, destination, departure, arrival, price)
  flights.setdefault((origin, destination), [])
  flights[(origin, destination)].append((departure, arrival, int(price)))

def print_calendar(calendar):
  flight_id = -1
  total_price = 0
  for i in range(len(calendar) // 2):
    name = passenger[i][0]
    # print(name)
    origin = passenger[i][1]
    # print(origin)
    flight_id += 1
    departure_flight = flights[(origin, destination)][calendar[flight_id]]
    # print(departure_flight)
    total_price += departure_flight[2]
    flight_id += 1
    arrival_flight = flights[(destination, origin)][calendar[flight_id]]
    total_price += arrival_flight[2]
    print('%10s%10s %5s-%5s U$%3s %5s-%5s U$%3s' % (name, origin, departure_flight[0], departure_flight[1], departure_flight[2], arrival_flight[0], arrival_flight[1], arrival_flight[2]))
  
  print('total price: ', total_price)

print_calendar([1,4, 3,2, 7,3, 6,3, 2,4, 5,3])

def get_minutes(hour):
  t = time.strptime(hour, '%H:%M')
  minutos = t[3] * 60 + t[4]
  return minutos

get_minutes('7:39'), get_minutes('10:32')

def evaluation_function(calendar):
  total_price = 0
  last_arrival = 0
  first_departure = 1439

  flight_id = -1
  for i in range(len(calendar) // 2):
    origin = passenger[i][1]
    flight_id += 1
    departure_flight = flights[(origin, destination)][calendar[flight_id]]
    flight_id += 1
    arrival_flight = flights[(destination, origin)][calendar[flight_id]]

    total_price += departure_flight[2]
    total_price += arrival_flight[2]

    if last_arrival < get_minutes(departure_flight[1]):
      last_arrival = get_minutes(departure_flight[1])
    if first_departure > get_minutes(arrival_flight[0]):
      first_departure = get_minutes(arrival_flight[0])

  total_wait_time = 0
  flight_id = -1
  for i in range(len(calendar) //2 ):
    origin = passenger[i][1]
    flight_id += 1
    departure_flight = flights[(origin, destination)][calendar[flight_id]]
    flight_id += 1
    arrival_flight = flights[(destination, origin)][calendar[flight_id]]

    total_wait_time += last_arrival - get_minutes(departure_flight[1])
    total_wait_time += get_minutes(arrival_flight[0]) - first_departure

    return total_wait_time + total_price

evaluation_function([1,4, 3,1, 8,3, 6,3, 2,4, 5,3])

domain = [(0, 9)] * (len(passenger) * 2)

#MUTATION ALGORITHM

def mutation(domain, rithm, calendar, probability):
  gene = random.randint(0, len(domain) -1)
  mutant = calendar
  if random.random() < probability: #probability number is better and realist between 2% (0.02) and  5% (0.05)
    if calendar[gene] != domain[gene][0]:
      mutant = calendar[0:gene] + [calendar[gene] - rithm] + calendar[gene + 1:]
    else:
       if calendar[gene] != domain[gene][1]:
         mutant = calendar[0:gene] + [calendar[gene] + rithm] + calendar[gene + 1:]
  return mutant

mutation(domain, 1, [6, 7, 6, 7, 3, 9, 7, 7, 0, 7, 6, 7], 0.05)

#CROSSOVER ALGORITHM

def crossover(domain, subject1, subject2):
  gene = random.randint(1, len(domain) - 2)
  # print(gene)
  return subject1[0:gene] + subject2[gene:]

s1 = [1,4, 3,2, 7,3, 6,3, 2,4, 5,3]
s2 = [0,1, 2,5, 8,9, 2,3, 5,1, 0,6]

crossover(domain, s1, s2)

#COMPLETE GENETIC ALGORITHM

def genetic_algorithm(domain, evaluation_function, population_size = 300, 
                       rithm = 1, elitism = 0.2, generations = 500, mutation_probability = 0.05):
  population = []
  for i in range(population_size):
    subject = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
    population.append(subject)
  elitism_number = int(elitism * population_size)

  for i in range(generations):
    custos = [(evaluation_function(subject), subject) for subject in population]
    custos.sort()
    subjects_order = [subject for (vusto, subject) in custos]
    population = subjects_order[0:elitism_number] # 0:2
    while len(population) < population_size:
      i1 = random.randint(0, elitism_number)
      i2 = random.randint(0, elitism_number)
      new_subject = crossover(domain, subjects_order[i1], subjects_order[i2])
      mutation_new_subject = mutation(domain, rithm, new_subject, mutation_probability)
      population.append(mutation_new_subject)

    # print('Population`s size: ', len(population))
  print(custos)
  return custos[0][1]

genetic_algorithm(domain, evaluation_function, generations = 3, population_size = 20, elitism = 0.4, mutation_probability = 0.5)

solution = genetic_algorithm(domain, evaluation_function, generations = 100, population_size = 100, 
                   elitism = 0.2, mutation_probability = 0.05)

evaluation_function(solution)

print_calendar(solution)

