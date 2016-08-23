from elements import Line, Text, Transform

class Graph(object):

  def __init__(self, width, height):
    self._width = width
    self._height = height
    self.defaults()

  def __init__(self, data = []):
    print "j"

  def defaults(self):
    self._margin = {
      "top"   : 0,
      "left"  : 0,
      "right" : 0,
      "bottom": 0
    }

    self.x_baseline = 0
    self.y_baseline = 0
    self.tick_length = 5

  @property
  def width(self):
    return self._width

  @width.setter
  def width(self, width):
    self._width = width

  @property
  def height(self):
    return self._height

  @width.setter
  def height(self, height):
    self._height = height

  def x_axis(self, ):
    print "x"