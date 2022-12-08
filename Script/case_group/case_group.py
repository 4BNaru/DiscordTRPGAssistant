from random import uniform
from collections import namedtuple

class case_group:
	case = []
	chance = []
	difficulty = []
	decided = None
	def __init__(self, *args):
		for i in args:
			self.case.append(namedtuple(i, -1))


	def decide_chance(self):
		weight = []
		for i in range(0, len(self.case)):
			weight.append(uniform(0, 1))

		sum = 0
		for i in weight:
			sum += i

		for i in weight:
			self.chance.append(i / sum * 100)

	def decide_case(self):
		dice = uniform(0, 100)

		#print(dice)
		#print(self.chance)

		i = 0
		sum_chance = self.chance[0]
		while(sum_chance < dice):
			i += 1
			sum_chance += self.chance[i]

		self.decided = self.case[i]

	def get_result(self) -> string:
		if self.decided is None:
			self.decide_case()
			return self.decided
		else:
			return self.decided

#c1 = case_group("name1", "name2", "name3", "name4")
#print(c1.get_result())
