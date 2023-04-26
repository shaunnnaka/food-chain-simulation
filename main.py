import random
import matplotlib.pyplot as plt

class Plant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(1, 5)
        self.growth_rate = random.uniform(0.1, 0.5)
        
    def grow(self):
        self.size += self.growth_rate
        
    def reproduce(self):
        if self.size > 10:
            return Plant(self.x + random.randint(-2, 2), self.y + random.randint(-2, 2))
        else:
            return None
        
class Animal:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.energy = random.uniform(0.5, 1.5)
        self.hunger = random.uniform(0.5, 1.5)
        
    def move(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = (dx**2 + dy**2)**0.5
        if dist > self.speed:
            dx = dx * self.speed / dist
            dy = dy * self.speed / dist
        self.x += dx
        self.y += dy
        self.energy -= 0.1
    
    def eat(self, plant):
        dx = plant.x - self.x
        dy = plant.y - self.y
        dist = (dx**2 + dy**2)**0.5
        if dist < self.speed:
            self.hunger -= plant.size
            self.energy += plant.size
            plant.size = 0
            return True
        else:
            return False
        
    def reproduce(self):
        if self.energy > 2 and self.hunger < 0.5:
            return Animal(self.x + random.randint(-2, 2), self.y + random.randint(-2, 2), self.speed)
        else:
            return None
        
class Insect:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.energy = random.uniform(0.5, 1.5)
        self.hunger = random.uniform(0.5, 1.5)
        
    def move(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = (dx**2 + dy**2)**0.5
        if dist > self.speed:
            dx = dx * self.speed / dist
            dy = dy * self.speed / dist
        self.x += dx
        self.y += dy
        self.energy -= 0.1
    
    def eat(self, plant):
        dx = plant.x - self.x
        dy = plant.y - self.y
        dist = (dx**2 + dy**2)**0.5
        if dist < self.speed:
            self.hunger -= plant.size / 2
            self.energy += plant.size / 2
            plant.size /= 2
            return True
        else:
            return False
        
    def reproduce(self):
        if self.energy > 1 and self.hunger < 1:
            return Insect(self.x + random.randint(-2, 2), self.y + random.randint(-2, 2), self.speed)
        else:
            return None


#animation
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
import seaborn as sns

size = 100
x = np.arange(size)
fig, ax = plt.subplots()
plt.close()
ax.set_xlim(( 0, 100))
ax.set_ylim((0, 100))
line, = ax.plot([],[],'b')


plants = []
for i in range(100):
  plants.append(Plant(random.uniform(0, 100), random.uniform(0, 100)))

animals = []
insects = []
for i in range(20):
  animals.append(Animal(random.uniform(0, 100), random.uniform(0, 100), random.uniform(1, 5)))
  insects.append(Insect(random.uniform(0, 100), random.uniform(0, 100), random.uniform(5, 10)))

for i in range(100):

  print("times: " + str(i))
  if(i == (30 or 10 or 25)):
    for i in range(10):
      animals.append(Animal(random.uniform(0, 100), random.uniform(0, 100), random.uniform(1, 5)))
      insects.append(Insect(random.uniform(0, 100), random.uniform(0, 100), random.uniform(5, 10)))

  # move animals and insects
  for animal in animals:
    target_plant = None
    for plant in plants:
      if animal.eat(plant):
        target_plant = plant
        print("animal < plant")
        break
      if target_plant is None:
        animal.move(random.uniform(0, 100), random.uniform(0, 100))
      else:
        animal.move(target_plant.x, target_plant.y)
        new_animal = animal.reproduce()

        if new_animal is not None:
          animals.append(new_animal)
          print("animal baby!")

  for insect in insects:
    target_plant = None
    for plant in plants:
      if insect.eat(plant):
        target_plant = plant
        print("insect < plant")

        break
      if target_plant is None:
        insect.move(random.uniform(0, 100), random.uniform(0, 100))
      else:
        insect.move(target_plant.x, target_plant.y)
        new_insect = insect.reproduce()
        if new_insect is not None:
          insects.append(new_insect)
        print("insect baby!")

  # grow plants
  for plant in plants:
      plant.grow()
      new_plant = plant.reproduce()
      if new_plant is not None:
          plants.append(new_plant)

  # remove dead plants and animals
  plants = [plant for plant in plants if plant.size > 0]
  animals = [animal for animal in animals if animal.energy > 0 and animal.hunger > 0]
  insects = [insect for insect in insects if insect.energy > 0 and insect.hunger > 0]
  print("live plants:" + str (len(plants) ))
  print("live animals:" + str (len(animals) ))
  print("live insects:" + str (len(insects) ))
  
  # plot the current state
  plt.clf()
  for plant in plants:
      plt.scatter(plant.x, plant.y, s=plant.size, c='green')
  for animal in animals:
      plt.scatter(animal.x, animal.y, s=15, c='read')
  for insect in insects:
      plt.scatter(insect.x, insect.y, s=10, c='orange')
  plt.xlim([0, 100])
  plt.ylim([0, 100])
  plt.title(f"Step {i}")
  #plt.draw()
  #plt.pause(0.01)
  plt.savefig("times" + str(i) + ".png")   