class Filter:

	def __init__(self):
		self.__prime_list = [2,3]
		self.__max_prime = 3
	
	def __generateUntilMinimum(self,last_num) :
		if(last_num > self.__max_prime):
			minimum_pass = False
			while not minimum_pass:
				self.__generateOne()
				if self.__max_prime > last_num:		
					minimum_pass = True

	def __isPrimeToList(self,x):		# поиск простых чисел
		for i in self.__prime_list:		# __prime_list = [2,3]	
			if x % i == 0:
				return False
		return True
			
	def __generateOne(self):				# перебор чисел от x = 3 с шагом x+2 
		prime_found = False
		candidate = self.__max_prime+2		# __max_prime = 3
		while not prime_found:
			if self.__isPrimeToList(candidate):
				self.__prime_list.append(candidate)
				self.__max_prime = candidate
				prime_found = True
			else:
				candidate = candidate + 2
	
	def getFirstPrimeLargerThan(self,x):
		if x >= self.__max_prime:
			self.__generateUntilMinimum(x+1)
			return self.__max_prime
