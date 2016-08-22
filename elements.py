from svg import SVG, SVGElement, SVGTextNode

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


class Path(SVG):
  def __init__(self):
    self._element = SVGElement("d")
  
  def render(self):
    return self._element.render()


class Transform(object):
  def __init__(self):
    self._degrees = 0
    self._transforms = {}

  def transform(self, x = 0, y = 0):
    template = "translate({0} {1})"
    self._transforms['translate'] = template.format(x, y)
        
  def rotate(self, degrees = 0, x = 0, y = 0):
    template = "rotate({0} {1} {2})"
    self._transforms['rotate'] = template.format(degrees, x, y)

  def render(self):
    values = ""
    for transform in self._transforms:
      values += self._transforms[transform] + " "

    return values.strip()

class Text(SVG):
  def __init__(self, text, x = 0, y = 0, dx = 0, dy = 0):
    self._element = SVGElement('text', inline = False)
    self._text = SVGTextNode(text)
    self._anchor = "middle"
    self._x = x
    self._y = y
    self._dx = dx
    self._dy = dy
    self._element.add(self._text)

  def shift(self, dx = 0, dy = 0):
    self._dx = dx
    self._dy = dy

  def transform(self, transform):
    self._element.addAttribute("transform", transform.render())

  def anchorStart(self):
    self._anchor = "start"

  def anchorMiddle(self):
        self._anchor = "middle"

  def anchorEnd(self):
        self._anchor = "end"

  def render(self):
    self._element.addAttribute("x", self._x)
    self._element.addAttribute("y", self._y)
    self._element.addAttribute("dx", str(self._dx) + "em")
    self._element.addAttribute("dy", str(self._dy) + "em")
    self._element.addAttribute("text-anchor", self._anchor)
    return self._element.render()
