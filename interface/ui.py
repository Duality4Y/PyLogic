import pygame
import pygame.freetype
import time

import os
import sys

pygame.init()
pygame.font.init()

moduleFilePath = os.path.abspath(sys.modules['__main__'].__file__)
projectRoot = os.path.dirname(moduleFilePath)

screenSize = screenWidth, screenHeight = 800, 600
screen = pygame.display.set_mode(screenSize)

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

Running = True

fontName = "Roboto-Regular.ttf"
fontSize = 18

fontResourcePath = os.path.join(projectRoot, "resources/fonts")
fontPath = os.path.join(fontResourcePath, fontName)
print(f"{__name__} : loading font: {fontPath}")
UIFont = pygame.freetype.Font(fontPath, fontSize)


class Alignment(object):
	def __init__(self):
		(self.center,
		 self.left,
		 self.right) = [i for i in range(0, 3)]
	"""
		calculate rect2 alignment relative to rect1 with padding
	"""
	def calcAlignment(self, rect1, rect2, alignment, padding):
		lx, ly, lwidth, lheight = rect1
		tx, ty, twidth, theight = rect2
		if alignment == self.center:
			x = int(lx + (lwidth - twidth) / 2)
			y = int(ly + (lheight - theight) / 2)
			return (x, y)
		if alignment == self.left:
			x = lx + padding
			y = int(ly + (lheight - theight) / 2)
			return (x, y)
		if alignment == self.right:
			x = lx + (lwidth - twidth) - padding
			y = int(ly + (lheight - theight) / 2)
			return (x, y) 
		return (0, 0)
Alignment = Alignment()

"""
	check if rect2 collides with rect1
"""
def CheckCollision(rect1, rect2):
	x1, y1, width1, height1 = rect1
	x2, y2, _, _ = rect2

	if (x2 > x1 and x2 < (x1 + width1)) and (y2 > y1 and y2 < (y1 + height1)):
		return True
	return False

# def EdgeDetector(object):
# 	def __init__(self):
# 		self.currState = 0
# 		self.prevState = 0
# 		(self.unchanging,
# 		 self.falling,
# 		 self.rising) = [i for i in range(0, 2)]
# 		self.state = self.unchanging

# 	def update(self, state):
# 		self.currState = state
# 		if self.currState > self.prevState:

""" Basic Widget object that determines what other elements should look like"""
class Widget(object):
	def __init__(self):
		self.offset = (0, 0)
		self.rect = (0, 0, 0, 0)

	def setOffset(self, offset):
		self.offset = offset

	def applyOffset(self, rect):
		xo, yo = self.offset
		x, y, width, height = rect
		return (x + xo, y + yo, width, height)

	""" This functions allows for the drawing of a border """
	def drawBorder(self, surface):
		pass
	""" This function draws the widget """
	def draw(self, surface):
		pass
	""" this function sets the internal state based on outside events."""
	def handleEvents(self, event):
		pass
	""" process previously set state to generate events and call calbacks if needed."""
	def processEvents(self):
		pass

class Pane(Widget):
	def __init__(self, rect):
		super().__init__()

		self.rect = rect

		self.borderVisible = True

		self.borderColor = GREEN
		self.border = 1
		self.borderWidth = 1

		self.widgets = []

	def addWidget(self, widget):
		self.widgets.append(widget)
		self.updateWidgets()

	def updateWidgets(self):
		for widget in self.widgets:
			x, y, _, _ = self.rect
			widget.setOffset((x, y))

	def drawBorder(self, surface):
		if self.borderVisible:
			x, y, width, height = self.rect
			rect = x, y, width, height
			# outer border is easy to draw it is just the bounding rectangle.
			pygame.draw.rect(surface, self.borderColor, rect, self.border)
			# calculate inner border and draw it
			inner = x + self.borderWidth + self.border * 2, \
					y + self.borderWidth + self.border * 2, \
					width - (self.borderWidth + self.border * 2) * 2, \
					height - (self.borderWidth + self.border * 2) * 2
			pygame.draw.rect(surface, self.borderColor, inner, self.border, border_radius=10)

	def draw(self, surface):
		self.drawBorder(surface)
		# for now set an offset to all the widgets relative to the pane and draw them
		for widget in self.widgets:
			widget.draw(surface)

	def handleEvents(self, event):
		super().handleEvents(event)
		for widget in self.widgets:
			widget.handleEvents(event)

	def processEvents(self):
		super().processEvents()
		for widget in self.widgets:
			widget.processEvents()



class Label(Widget):
	def __init__(self, text="", textAlignment=Alignment.center, borderVisible=True):
		super().__init__()
		self.text = text
		# self.textColor = WHITE
		self.textColor = tuple([0xff] * 3)
		self.border = 2
		self.borderColor = BLUE

		self.borderVisible = borderVisible

		# how much room between edge and text (padding between text and label border)
		self.defaultPadding = 8
		self.padding = self.defaultPadding

		self.textAlignment = textAlignment
		self.textSurface, self.textRect = UIFont.render(self.text, self.textColor)
		_, _, textWidth, textHeight = self.textRect
		self.rect = (0, 0, textWidth * 1.5 + self.defaultPadding, textHeight * 1.5 + self.defaultPadding)

	def drawBorder(self, surface):
		""" Draw a border rectangular. """
		if(self.borderVisible):
			pygame.draw.rect(surface, self.borderColor, self.rect, self.border)
	
	def draw(self, surface):
		""" Draw the text after applying a alignment function to its position. """
		x, y = Alignment.calcAlignment(self.rect, self.textRect, self.textAlignment, self.padding)
		surface.blit(self.textSurface, (x, y))
		""" draw a border """
		self.drawBorder(surface)

class Button(Label):
	def __init__(self):
		super().__init__("Button")
		self.mpos = 0, 0

		""" Custom label properties for a button. """
		self.borderPadding = self.border * 2
		_, _, textWidth, textHeight = self.textRect
		self.rect = (50, 50, textWidth * 1.5 + self.defaultPadding + self.borderPadding, textHeight * 1.5 + self.defaultPadding + self.borderPadding)
		self.borderColor = [169] * 3
		self.textAlignment = Alignment.center

		self.clickState = 0
		self.prevClickState = 0

		self.onPressed = None
		self.onReleased = None

		self.pressedCallback = None
		self.releasedCallback = None

	def setClickState(self, clickState):
		self.clickState = clickState

	def isPressed(self):
		return (self.clickState > self.prevClickState)

	def isReleased(self):
		return (self.clickState < self.prevClickState)

	def drawBorder(self, surface):
		""" Draw a border rectangular. """
		if(self.borderVisible):
			x, y, width, height = self.rect
			smallest = min(width, height)
			pygame.draw.rect(surface, self.borderColor, self.rect, self.border, round(smallest / 3))

	def draw(self, surface):
		super().draw(surface)

	def handleEvents(self, event):
		leftMouseBtn, _, _ = pygame.mouse.get_pressed()
		self.setClickState(leftMouseBtn)
		if event.type == pygame.MOUSEMOTION:
			self.mpos = event.pos

	def processEvents(self):
		colliding = CheckCollision(self.applyOffset(self.rect), (*self.mpos, 0, 0))
		if colliding:
			if self.isPressed():
				if self.pressedCallback:
					self.pressedCallback(self)
		""" 
			Always check for a button release even outside of the button
			because the mouse pointer can held down and moved outside of the button.
		"""
		if self.isReleased():
			if self.releasedCallback:
				self.releasedCallback(self)

		self.prevClickState = self.clickState

class CheckButton(Button):
	def __init__(self):
		super().__init__()
		self.marked = False
		self.prevMarked = False

		self.checkCallback = None
		self.pressedCallback = self.OnPressed

		self.buttonSetColor = GREEN
		self.buttonSetColor = [0, 0xff >> 1, 0]
		"""
			if highLightBorder has a value high then zero an highlight border that size is draw
			if highLightBorder is zero then the rect is filled.
		"""
		self.highLightBorder = 0

	def OnPressed(self, widget):
		self.marked = not self.marked

	def draw(self, surface):
		""" fill in the button if button is set. """
		if(self.marked):
			if(self.borderVisible):
				_, _, width, height = self.rect
				smallest = min(width, height)
				pygame.draw.rect(surface, self.buttonSetColor, self.applyOffset(self.rect), self.highLightBorder, round(smallest / 3))
		""" Draw the normal border to indicate it's a button. """
		super().draw(surface)

	def handleEvents(self, event):
		super().handleEvents(event)

	def processEvents(self):
		super().processEvents()
		if self.prevMarked != self.marked:
			if self.checkCallback:
				self.checkCallback(self)
		self.prevMarked = self.marked

class Grid(Widget):
	pass

class App(Widget):
	def __init__(self):
		self.Running = True
		self.widgets = []

	def addWidget(self, widget):
		self.widgets.append(widget)

	def quitApplication(self):
		pygame.quit()
		quit()

	def run(self):
		while self.Running:
			""" handle all the events. """
			for event in pygame.event.get():
				for widget in self.widgets:
					widget.handleEvents(event)
				""" Exit on pressing escape. """
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.Running = False
				""" Exit on hitting the window X. """
				if event.type == pygame.QUIT:
					self.Running = False
			""" process and draw all the events."""
			screen.fill(BLACK)
			for widget in self.widgets:
				widget.processEvents()
				widget.draw(screen)
			pygame.display.flip()
		self.quitApplication()

class TestApp(App):
	def __init__(self):
		super().__init__()

		# button = Button()
		# button.pressedCallback = self.pressedCallback
		# button.releasedCallback = self.releasedCallback
		# self.addWidget(button)

		button = CheckButton()
		button.checkCallback = self.checkCallback
		# self.addWidget(button)
		
		# label = Label("Hello, World!")
		# self.addWidget(label)

		# texts = 	 ["Left", "Center", "Right"]
		# alignments = [Alignment.left, Alignment.center, Alignment.right]
		# for i, (text, alignment) in enumerate(zip(texts, alignments)):
		# 	x = 50
		# 	y = 260 + (i * 60)
		# 	label = Label(text=text, textAlignment=alignment)
		# 	_, _, Lwidth, Lheight = label.rect
		# 	# multiply label width by 2 to exaggerate allignment
		# 	label.rect = x, y, Lwidth * 2, Lheight
		# 	self.addWidget(label)

		pane = Pane((0, screenHeight / 2, screenWidth, screenHeight / 2))
		pane.addWidget(button)
		self.addWidget(pane)

	def checkCallback(self, widget):
		print(f"checkState: {widget.marked}")

	def pressedCallback(self, widget):
		print(f"pressed {widget}")

	def releasedCallback(self, widget):
		print(f"released {widget}")
