from colorama import init, Fore
init(convert=True)
## select higher level products you want to count
listOfMainBusResources = ["copper plate","iron plate","electronic circuit"]

## select globally type of furnaces used
furnacesDict = {
	"Stone" : 1,
	"Steel" : 2
}
furnaceType = "Steel" # <- type of furnace


## select globally level of assembling machines used
assemblingMachinesDict = {
	1 : 0.5,
	2 : 0.75
}
assemblingMachineLevel = 2 # <- level of assembling machine

########## Ingredient class ##########
class Ingredient:
	def __init__(self, initName, initStation, initCraftedPerSecond = None , initCraftingTime = None , initCraftedAmount = 1):
		self.name = initName 
		self.craftedPerSecond = initCraftedPerSecond
		self.craftedTimes = (initCraftingTime/initCraftedAmount)*(initStation, 1)[initStation is None]
		self.color = Fore.WHITE
		
	def getIngredients_inner(self):
		return [[self, self.craftedPerSecond]]
		
	def __str__(self):
		return "%s %.2f units of %s per second" % (self.color, self.craftedPerSecond , self.name)
		
	def getIngredients(self):
		return self
########### Station class ############
class Station:
	def __init__(self, initName, initSpeedModifier):
		self.name = initName
		self.speedModifier = initSpeedModifier
	
	def __mul__(self, other):
		return other/self.speedModifier
		
	__rmul__=__mul__

class AssemblingMachine(Station):
	def __init__(self): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), assemblingMachinesDict[assemblingMachineLevel])

class Furnace(Station):
	def __init__(self): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), furnacesDict[furnaceType])

class Chemical_plant(Station):
	def __init__(self): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), 1)

class Oil_refinery(Station):
	def __init__(self): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), 1)

class Copper_ore(Ingredient):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.YELLOW

class Iron_ore(Ingredient):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.CYAN

class Coal(Ingredient):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.WHITE
	
class Stone(Ingredient):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.WHITE

class Wood(Ingredient):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.YELLOW

class Crude_oil(Ingredient):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.WHITE

class Water(Ingredient):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.BLUE
########### Product class ############
class Product(Ingredient):
	def __init__(self, initName, initStation = None, initCraftedPerSecond = None , initCraftingTime = None , initCraftedAmount = 1):
		Ingredient.__init__(self, initName, initStation, initCraftedPerSecond, initCraftingTime, initCraftedAmount)
	listOfComponents = None
	
	def getIngredients_inner(self):
		tempListOfIngredients = []
		listOfIngredients = []
		for singleIngredient in self.listOfComponents:
			if singleIngredient[0].name in listOfMainBusResources:
				tempListOfIngredients.append([singleIngredient[0],singleIngredient[1]])
				continue
			temp = singleIngredient[0].getIngredients_inner()								
			for temporarySingleIngredient in temp:
				tempListOfIngredients.append(temporarySingleIngredient)
		for singleIngredient in tempListOfIngredients:
			for index, ingredientFromList in enumerate(listOfIngredients):
				if type(singleIngredient[0]) == type(ingredientFromList[0]):
					listOfIngredients[index][1] += singleIngredient[1]
					break
			else:
				listOfIngredients.append(singleIngredient)
		return listOfIngredients

	def __str__(self):
		temp = ""
		for singleIngredient in self.listOfComponents:
			temp += "\n\t" + str(singleIngredient[0]).replace("\n","\n\t")
		return "%s %.2f units of %s per second that requires" % (self.color, self.craftedPerSecond, self.name) + temp

	def getIngredients(self):
		listOfIngredients = self.getIngredients_inner()
		temp = ""
		for singleIngredient in listOfIngredients:
			temp += "\n\t%s %.2f units of %s per second" % (singleIngredient[0].color, singleIngredient[1] , singleIngredient[0].name)
		return "%s To get %.2f units of %s per second you need" % (self.color, self.craftedPerSecond , self.name) + temp

class Copper_plate(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 3.2 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), Furnace(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Copper_ore(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond],[Coal(initCraftedPerSecond=self.craftedTimes*0.0720461095100865),0.0720461095100865*self.craftedPerSecond]]

class Iron_plate(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 3.2 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), Furnace(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.CYAN
		self.listOfComponents = [[Iron_ore(initCraftedPerSecond*1),1*self.craftedPerSecond],[Coal(initCraftedPerSecond*0.0720461095100865),0.0720461095100865*self.craftedPerSecond]]

class Iron_gear_wheel(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.CYAN
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedPerSecond]]

class Copper_cable(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.CYAN
		self.listOfComponents = [[Copper_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond]]

class Electronic_circuit(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.GREEN
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Copper_cable(initCraftedPerSecond=self.craftedTimes*3),3*self.craftedPerSecond]]

class Automation_science_pack(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.RED
		self.listOfComponents = [[Copper_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond]]

class Transport_belt(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.WHITE
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond]]

class Inserter(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond],[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond]]

class Logistic_science_pack(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 6 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.GREEN
		self.listOfComponents = [[Transport_belt(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Inserter(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond]]

class Steel_plate(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 16 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), Furnace(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.WHITE
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedTimes],[Coal(initCraftedPerSecond=self.craftedTimes*0.3610108303249097),0.3610108303249097*self.craftedPerSecond]]

class Solar_panel(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 10 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.BLUE
		self.listOfComponents = [[Copper_plate(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedTimes],[Steel_plate(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedPerSecond],[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*15),15*self.craftedPerSecond]]

class Repair_pack(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.WHITE
		self.listOfComponents = [[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedPerSecond]]

class Long_handed_inserter(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.RED
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond],[Inserter(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond]]

class Fast_inserter(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.RED
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedPerSecond],[Inserter(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond]]

class Firearm_magazine(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.RED
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*4),4*self.craftedTimes]]

class Assembling_machine_1(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*9),9*self.craftedTimes],[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedPerSecond],[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*3),3*self.craftedPerSecond]]

class Assembling_machine_2(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.BLUE
		self.listOfComponents = [[Steel_plate(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedPerSecond],[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*3),3*self.craftedPerSecond],[Assembling_machine_1(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond]]

class Iron_stick(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.WHITE
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes]]

class Transport_belt(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Iron_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes]]

class Underground_belt(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*10),10*self.craftedTimes],[Transport_belt(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedTimes]]

class Splitter(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedTimes],[Iron_plate(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedTimes],[Transport_belt(initCraftedPerSecond=self.craftedTimes*4),4*self.craftedTimes]]

class Fast_transport_belt(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.RED
		self.listOfComponents = [[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedTimes],[Transport_belt(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes]]

class Fast_underground_belt(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 2 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.RED
		self.listOfComponents = [[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*40),40*self.craftedTimes],[Underground_belt(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes]]

class Fast_splitter(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 2 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.RED
		self.listOfComponents = [[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*10),10*self.craftedTimes],[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*10),10*self.craftedTimes],[Splitter(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes]]

class Fast_inserter(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Inserter(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Iron_plate(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes]]

class Piercing_rounds_magazine(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 6 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.RED
		self.listOfComponents = [[Copper_plate(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Firearm_magazine(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Steel_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes]]

class Grenade(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 8 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.CYAN
		self.listOfComponents = [[Coal(initCraftedPerSecond=self.craftedTimes*10),10*self.craftedTimes],[Iron_plate(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedTimes]]

class Petroleum_gas(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 5 , initCraftedAmount = 45): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), Oil_refinery(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.WHITE
		self.listOfComponents = [[Crude_oil(initCraftedPerSecond=self.craftedTimes*100),100*self.craftedTimes]]

class Sulfur(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), Chemical_plant(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Petroleum_gas(initCraftedPerSecond=self.craftedTimes*30),30*self.craftedTimes],[Water(initCraftedPerSecond=self.craftedTimes*30),30*self.craftedTimes]]

class Plastic_bar(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), Chemical_plant(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Coal(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Petroleum_gas(initCraftedPerSecond=self.craftedTimes*20),20*self.craftedTimes]]

class Sulfuric_acid(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 50): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), Chemical_plant(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Sulfur(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedTimes],[Water(initCraftedPerSecond=self.craftedTimes*100),100*self.craftedTimes]]

class Explosives(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 4 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Coal(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Sulfur(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Water(initCraftedPerSecond=self.craftedTimes*10),10*self.craftedTimes]]

class Advanced_circuit(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 6 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.RED
		self.listOfComponents = [[Copper_cable(initCraftedPerSecond=self.craftedTimes*4),4*self.craftedTimes],[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Plastic_bar(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes]]

class Pipe(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.WHITE
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes]]

class Engine_unit(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 10 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.WHITE
		self.listOfComponents = [[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Pipe(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Steel_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes]]

class Chemical_science_pack(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 24 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.CYAN
		self.listOfComponents = [[Advanced_circuit(initCraftedPerSecond=self.craftedTimes*3),3*self.craftedTimes],[Engine_unit(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Sulfur(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes]]

class Battery(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 4 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), Chemical_plant(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.WHITE
		self.listOfComponents = [[Copper_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Iron_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Sulfuric_acid(initCraftedPerSecond=self.craftedTimes*20),20*self.craftedTimes]]

class Processing_unit(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 10 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), Chemical_plant(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.WHITE
		self.listOfComponents = [[Advanced_circuit(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*20),20*self.craftedTimes],[Sulfuric_acid(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedTimes]]

class Rocket(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 4 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Explosives(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Iron_plate(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes]]

class Explosive_rocket(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 8 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.RED
		self.listOfComponents = [[Explosives(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Explosives(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes]]

class Cannon_shell(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 8 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Explosives(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Plastic_bar(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Steel_plate(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes]]

class Explosive_cannon_shell(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 8 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Explosives(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Plastic_bar(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Steel_plate(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes]]

class Poison_capsule(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 8 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.BLUE
		self.listOfComponents = [[Coal(initCraftedPerSecond=self.craftedTimes*10),10*self.craftedTimes],[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*3),3*self.craftedTimes],[Steel_plate(initCraftedPerSecond=self.craftedTimes*3),3*self.craftedTimes]]

class Slowdown_capsule(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 8 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), AssemblingMachine(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Coal(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedTimes],[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Steel_plate(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes]]

class Flamethrower_ammo(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 6 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," "), Chemical_plant(), initCraftedPerSecond, initCraftingTime, initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Crude_oil(initCraftedPerSecond=self.craftedTimes*100),100*self.craftedTimes],[Steel_plate(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedTimes]]
