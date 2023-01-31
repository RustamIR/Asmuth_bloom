from filter import Filter
from chinese_remainder import chinese_remainder
import random
import time

# создаем объект держателей секрета
class Holder:
	
	def __init__(self):
		# проекция
		self.module = 0
		# секрет
		self.secret = 0


	def __str__(self):
		return "Проекция = " + str(self.module) + " | Секрет = " + str(self.secret)


# объект схемы Асмута-Блума
class Asmuth_Bloom:
	
	def __init__(self, n_holders_, min_holder, secret, verbose=False):
		self.__verbose = verbose
		self.filter = Filter()
		self.n_holders_ = n_holders_								# всего хранителей секрета
		self._min_holder = min_holder							# допустимый минимум хранителей для расшифровки секрета
		self._hoders = [Holder() for _ in range(n_holders_)]
		self.__secret = secret
		self.generateHolders()

	# проекция и часть секрета для каждого пользователя
	def generateHolders(self):
		self.generate_Sequence()
		self.generate_Random()


		for i in range(self.n_holders_) :
			self._hoders[i].module = self.__sequence[i+1]
			self._hoders[i].secret = self.__y % self._hoders[i].module

	def generate_Sequence(self):
	
		initial_multiplier = self.__secret//10
		# Получите первое простое число в последовательности
		first_prime = self.filter.getFirstPrimeLargerThan(self.__secret)

		sequenceValid = False
		
		# Получите остальную часть последовательности
		while not sequenceValid :
			current_sequence = [first_prime]
			print(f'current_sequence = {current_sequence}')
			temp_prime = self.filter.getFirstPrimeLargerThan(self.__secret * initial_multiplier)
			print(f'temp_prime = {temp_prime}')
			for _ in range(self.n_holders_) :
				temp_prime = self.filter.getFirstPrimeLargerThan(temp_prime)
				print(f'temp_prime ={temp_prime}')
				current_sequence.append(temp_prime)
			
			if self.is_Sequence_Valid(current_sequence):
				sequenceValid = True
			
			else: 
				initial_multiplier = initial_multiplier + 1
				
		print(f'current_sequence = {current_sequence}')
		self.__sequence = current_sequence
		print(f'self.__sequence[1:self._min_holder+1] = {self.__sequence[1:self._min_holder+1]}')
		self.__M = self.seqprod(self.__sequence[1:self._min_holder+1])
		
		if self.__verbose:
			print(f"M = m1*m2*...*mn = {str(self.__M)}")
	

	# Генератор рандомных чисел
	def generate_Random(self):
		max = int((self.__M - self.__secret)/self.__sequence[0])
		
		self.e_i = random.randint(1,max)
		self.__y = self.__secret + self.e_i * self.__sequence[0]
		if self.__verbose :
			print(f"Рандомное число: e = {str(self.e_i)}")
			print(f"Y-значение : {str(self.__y)}")

	### UTILS
	def is_Sequence_Valid(self, seq):
		lower_product = self.seqprod(seq[1:self._min_holder+1])
		upper_product = seq[0]*self.seqprod(seq[self.n_holders_ - self._min_holder + 2:])

		return lower_product > upper_product
		

	# своя функция reduce()
	def seqprod(self, iterable):
		product = 1
		for item in iterable:
			product = product * item
		return product
		

	def getHolders(self):
		return self._hoders
		

	### решение
	def solve(self):
		
		# выбранные держатели секрета
		chosen_holders = random.sample(self._hoders, self._min_holder)		# _hoders - список хранителей секрета, _min_holder - vминимальное кол. хранителей секрета
		
		if self.__verbose :
			print("Минимально требуемое количество держателей секрета:")
			for holder in chosen_holders :
				print(holder)
		
		## решение CRT
		modulo_list = [holder.module for holder in chosen_holders]			# список Modulo
		remainder_list = [holder.secret for holder in chosen_holders]		# список секретов каждого Modulo
		
		
		solution = chinese_remainder(modulo_list, remainder_list)
		if self.__verbose:
			print("CRT Solution: " + str(solution))

		return (solution) % self.__sequence[0]
	

def main():	
	number_of_holders = int(input("Введите количество держателей секрета: "))

	while number_of_holders < 1:
		number_of_holders = int(input("Число должно быть больше единицы. Пробуйте снова: "))
	min_number_to_solve = int(input("Введите минимальное количество держателей для извлечения секрета: " ))

	while min_number_to_solve > number_of_holders or min_number_to_solve < 1:
		min_number_to_solve = int(input("Минимальное количество должно составлять от 1 до количества держателей. Пробуйте снова: "))
	
	secret = int(input("Введите секрет: "))
	while secret < 0 :
		secret = int(input("Секрет не должен быть меньше нуля. Пробуйте снова: "))
	
	# generation_start = time.time()
	S = Asmuth_Bloom(number_of_holders, min_number_to_solve, secret, verbose=True)
	# generation_end = time.time()

	# Вывести держателей секрета
	print('все хранители секрета')
	for holder in S.getHolders():
		print(f'{holder}')
		

	# solve_start = time.time()
	secret = S.solve()
	# solve_end = time.time()

	# print("Время шифровки (с): " + str(generation_end - generation_start))
	# print("Время расшифровки (с): " + str(solve_end - solve_start))
	
	print(f'secret = {secret}')

main()
