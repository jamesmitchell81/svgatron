from svg import SVG, SVGElement

class Line(SVG):
  def __init__(self, x1, x2, y1, y2):
    self._element = SVGElement("line")
    self.create(x1, x2, y1, y2)
    self._stroke = "black"
    self._strokeWidth = 1

  def stroke(self, stroke = "black"):
    self._stroke = stroke

  def strokeWidth(self, strokeWidth = 1):
    self._strokeWidth = strokeWidth

  def create(self, x1 = 0, x2 = 0, y1 = 0, y2 = 0):
    self._element.addAttribute("x1", x1)
    self._element.addAttribute("y1", y1)
    self._element.addAttribute("x2", x2)
    self._element.addAttribute("y2", y2)

  def addAttribute(self, key, value):
    self._element.addAttribute(key, value)

  def render(self):
    self._element.addAttribute("stroke", self._stroke)
    self._element.addAttribute("stroke-width", self._strokeWidth)
    return self._element.render()

class Rect(SVG):
  def __init__(self):
    self._element = SVGElement("rect")

  def render(self):
    return self._element.render()


