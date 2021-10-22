"""
	Basic class for description of a part
	like how many inputs and outputs it has
	and what the names are of those inputs/outputs
	and what the name is for that part.

	e.g. a And gate has 2 inputs and 1 output
	and a latch 2 inputs and 2 outputs.

	by making this a class to be inherited from 
	you could use it to dynamically generate tests or do other things with it.
"""

class Part(object):
	def __init__(self, numInputs=0, numOutputs=0, name="Unknown", lines=["Not", "available"]):
		self.numInputs = numInputs
		self.numOutputs = numOutputs

		self.inputs = []
		self.outputs = []
		
		self._name = name
		self.lines = lines

		self._alignsize = max(len(item) for item in lines) + 1
		self._fmt = "{{0:{0}}}".format(self._alignsize)
		self._tableSeperator = "|"

	@property
	def name(self):
		return self._name

	def buildTable(self, elements):
		return self._tableSeperator.join(self._fmt.format(str(element)) for element in elements)

	def getLineTable(self):
		return self.buildTable(self.lines)

	def setInput(self, *args):
		pass

	def getOutput(self):
		return None

	def process(self):
		pass

	def __repr__(self):
		return "Basic Part no states"