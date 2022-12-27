from random import uniform

class Case_group:
	case = []
	chance = []
	difficulty = []
	decided = None
	def __init__(self, args = []):
		self.case = args
		self.difficulty = [-1] * len(args)
		self.decide_chance()

	def decide_chance(self):
		weight = []
		for i in range(0, len(self.case)):
			weight.append(uniform(0, 1))

		sumary = sum(weight)

		for i in weight:
			self.chance.append(i / sumary * 100)

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

	def get_result(self) -> str:
		if self.decided is None:
			self.decide_case()
			return self.decided
		else:
			return self.decided

#c1 = case_group("name1", "name2", "name3", "name4")
#print(c1.get_result())
