from colorama import init, Fore
init(convert=True)


## select globally type of furnaces used
furnacesDict = {
	"Stone" : 1,
	"Steel" : 2
}
furnaceType = "Steel" # <- type of furnace


## select globally level of assembly machines used
assemblyMachinesDict = {
	1 : 0.5,
	2 : 0.75
}
assemblyMachineLevel = 2 # <- type of furnace


class Ingredient:
	def __init__(self, initName, initCraftedPerSecond = None , initCraftingTime = None , initCraftedAmount = 1):
		self.name = initName 
		self.craftedPerSecond = initCraftedPerSecond
		self.craftedTimes = initCraftedPerSecond/initCraftedAmount
		self.color = Fore.WHITE
		
	def getBasicIngredients_inner(self):
		return [[self, self.craftedPerSecond]]
		
	def getMainBusIngredients_inner(self):
		return [[self, self.craftedPerSecond]]
		
	def __str__(self):
		return "%s %.2f pieces of %s per second" % (self.color, self.craftedPerSecond , self.name)
		
	def getBasicIngredients(self):
		return "%s %.2f pieces of %s per second" % (self.color, self.craftedPerSecond , self.name)

	def getMainBusIngredients(self):
		return "%s %.2f pieces of %s per second" % (self.color, self.craftedPerSecond , self.name)

class Copper_ore(Ingredient):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.YELLOW

class Iron_ore(Ingredient):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.CYAN

class Coal(Ingredient):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.WHITE
	
class Stone(Ingredient):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.WHITE

class Wood(Ingredient):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.YELLOW

class Product(Ingredient):
	def __init__(self, initName, initCraftedPerSecond = None , initCraftingTime = None , initCraftedAmount = 1):
		Ingredient.__init__(self, initName , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
	listOfComponents = None
	
	def getBasicIngredients_inner(self):
		tempListOfIngredients = []
		listOfIngredients = []
		for singleIngredient in self.listOfComponents:
			temp = singleIngredient[0].getBasicIngredients_inner()								
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

	def getMainBusIngredients_inner(self):
		tempListOfIngredients = []
		listOfIngredients = []
		for singleIngredient in self.listOfComponents:
			temp = singleIngredient[0].getMainBusIngredients_inner()								
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
		return "%s %.2f pieces of %s per second that requires" % (self.color, self.craftedPerSecond, self.name) + temp
	
	def getBasicIngredients(self):
		listOfIngredients = self.getBasicIngredients_inner()
		temp = ""
		for singleIngredient in listOfIngredients:
			temp += "\n\t%s %.2f pieces of %s per second" % (singleIngredient[0].color, singleIngredient[1] , singleIngredient[0].name)
		return "%s To get %.2f pieces of %s per second you need" % (self.color, self.craftedPerSecond , self.name) + temp
		
	def getMainBusIngredients(self):
		listOfIngredients = self.getMainBusIngredients_inner()
		temp = ""
		for singleIngredient in listOfIngredients:
			temp += "\n\t%s %.2f pieces of %s per second" % (singleIngredient[0].color, singleIngredient[1] , singleIngredient[0].name)
		return "%s To get %.2f pieces of %s per second you need" % (self.color, self.craftedPerSecond , self.name) + temp

class Main_bus_ingredient(Product):
	def __init__(self, initName, initCraftedPerSecond = None , initCraftingTime = None , initCraftedAmount = 1):
		Ingredient.__init__(self, initName , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
	listOfComponents = None
	
	def getBasicIngredients_inner(self):
		tempListOfIngredients = []
		listOfIngredients = []
		for singleIngredient in self.listOfComponents:
			temp = singleIngredient[0].getBasicIngredients_inner()								
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
	
	def getMainBusIngredients_inner(self):
		return [[self, self.craftedPerSecond]]
		
	def __str__(self):
		temp = ""
		for singleIngredient in self.listOfComponents:
			temp += "\n\t" + str(singleIngredient[0]).replace("\n","\n\t")
		return "%s %.2f pieces of %s per second that requires" % (self.color, self.craftedPerSecond, self.name) + temp
	
	def getBasicIngredients(self):
		listOfIngredients = self.getBasicIngredients_inner()
		temp = ""
		for singleIngredient in listOfIngredients:
			temp += "\n\t%s %.2f pieces of %s per second" % (singleIngredient[0].color, singleIngredient[1] , singleIngredient[0].name)
		return "%s To get %.2f pieces of %s per second you need" % (self.color, self.craftedPerSecond , self.name) + temp
		
	def getMainBusIngredients(self):
		listOfIngredients = self.getMainBusIngredients_inner()
		temp = ""
		for singleIngredient in listOfIngredients:
			temp += "\n\t%s %.2f pieces of %s per second" % (singleIngredient[0].color, singleIngredient[1] , singleIngredient[0].name)
		return "%s To get %.2f pieces of %s per second you need" % (self.color, self.craftedPerSecond , self.name) + temp

class Copper_plate(Main_bus_ingredient):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 3.2 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Copper_ore(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond],[Coal(initCraftedPerSecond=self.craftedTimes*0.0720461095100865),0.0720461095100865*self.craftedPerSecond]]

class Iron_plate(Main_bus_ingredient):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 3.2 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.CYAN
		self.listOfComponents = [[Iron_ore(initCraftedPerSecond*1),1*self.craftedPerSecond],[Coal(initCraftedPerSecond*0.0720461095100865),0.0720461095100865*self.craftedPerSecond]]

class Iron_gear_wheel(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.CYAN
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedPerSecond]]

class Copper_cable(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.CYAN
		self.listOfComponents = [[Copper_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond]]

class Electronic_circuit(Main_bus_ingredient):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.GREEN
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Copper_cable(initCraftedPerSecond=self.craftedTimes*3),3*self.craftedPerSecond]]

class Automation_science_pack(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.RED
		self.listOfComponents = [[Copper_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond]]

class Transport_belt(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.WHITE
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond]]

class Inserter(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond],[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond]]

class Logistic_science_pack(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 6 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.GREEN
		self.listOfComponents = [[Transport_belt(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Inserter(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond]]

class Steel_plate(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 16 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.WHITE
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedTimes],[Coal(initCraftedPerSecond=self.craftedTimes*0.3610108303249097),0.3610108303249097*self.craftedPerSecond]]

class Solar_panel(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 10 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.BLUE
		self.listOfComponents = [[Copper_plate(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedTimes],[Steel_plate(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedPerSecond],[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*15),15*self.craftedPerSecond]]

class Repair_pack(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.WHITE
		self.listOfComponents = [[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedPerSecond]]

class Long_handed_inserter(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.RED
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond],[Inserter(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond]]

class Fast_inserter(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.RED
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedPerSecond],[Inserter(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond]]

class Firearm_magazine(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.RED
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*4),4*self.craftedTimes]]

class Assembling_machine_1(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*9),9*self.craftedTimes],[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedPerSecond],[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*3),3*self.craftedPerSecond]]

class Assembling_machine_2(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.BLUE
		self.listOfComponents = [[Steel_plate(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedPerSecond],[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*3),3*self.craftedPerSecond],[Assembling_machine_1(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedPerSecond]]

class Iron_stick(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.WHITE
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes]]

class Transport_belt(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Iron_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes]]

class Underground_belt(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Iron_plate(initCraftedPerSecond=self.craftedTimes*10),10*self.craftedTimes],[Transport_belt(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedTimes]]

class Splitter(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 1 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedTimes],[Iron_plate(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedTimes],[Transport_belt(initCraftedPerSecond=self.craftedTimes*4),4*self.craftedTimes]]

class Fast_transport_belt(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.RED
		self.listOfComponents = [[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedTimes],[Transport_belt(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes]]

class Fast_underground_belt(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 2 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.RED
		self.listOfComponents = [[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*40),40*self.craftedTimes],[Underground_belt(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes]]

class Fast_splitter(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 2 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.RED
		self.listOfComponents = [[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*10),10*self.craftedTimes],[Iron_gear_wheel(initCraftedPerSecond=self.craftedTimes*10),10*self.craftedTimes],[Splitter(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes]]

class Fast_inserter(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = .5 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.YELLOW
		self.listOfComponents = [[Electronic_circuit(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Inserter(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes],[Iron_plate(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes]]

class Piercing_rounds_magazine(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 6 , initCraftedAmount = 2): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.RED
		self.listOfComponents = [[Copper_plate(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Firearm_magazine(initCraftedPerSecond=self.craftedTimes*2),2*self.craftedTimes],[Steel_plate(initCraftedPerSecond=self.craftedTimes*1),1*self.craftedTimes]]

class Grenade(Product):
	def __init__(self, initCraftedPerSecond = None , initCraftingTime = 8 , initCraftedAmount = 1): 
		super().__init__( (type(self).__name__).lower().replace("_"," ") , initCraftedPerSecond , initCraftingTime , initCraftedAmount)
		self.color = Fore.CYAN
		self.listOfComponents = [[Coal(initCraftedPerSecond=self.craftedTimes*10),10*self.craftedTimes],[Iron_plate(initCraftedPerSecond=self.craftedTimes*5),5*self.craftedTimes]]
