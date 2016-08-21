class SVG:
  def render(self):
    raise NotImplementedError("'render' method required")

class SVGRoot(SVG):
  def __init__(self):
    self._xmlns = "http://www.w3.org/2000/svg" 
    self._tag = "svg"
    self._viewbox = ""
    self._width = ""
    self._height = ""
    self._children = []

  def addElement(self, element):
    if hasattr(element.render, '__call__'):
      # TODO: raise exception where no render
      self._children.append(element)

  def render(self):
    formatted = self.open()
    # render children
    for child in self._children:
      formatted += child.render()

    formatted += self.close()
    return formatted

  def open(self):
    s = ('<%(_tag)s'
          ' viewBox="%(_viewbox)s"'
          ' width="%(_width)s" height="%(_height)s"'
          ' xmlns="%(_xmlns)s"'
          '>\n'
          )
    return s % self.__dict__

  def close(self):
    return '</{0}>'.format(self._tag)


class SVGElement(SVG):
  def __init__(self, tag, id = ""):
    self._tag = tag
    self._id = ""
    self.children = []
    self.class_list = []
    self.attributes = []

  @property
  def tag(self):
    return self._tag

  @tag.setter
  def tag(self, tag):
    self._tag = tag

  @property
  def id(self, id):
    return self._id

  @id.setter
  def id(self, id):
    self._id = id

  def addElement(self, element):
    self.children.append(element)

  def addAttribute(self, key, value):
    self.attributes.append({ key: value})

  def addClass(self, class_name):
    self.classes.append(class_name)

  def render(self):
    if self._inline:
      return self.renderInline()

    return self.renderBlock()

  def renderInline(self):
    print "inline"

  def renderBlock(self):
    elem = self.open()
    for child in self.children:
      elem += child.render()

    return elem + self.close()

  def open(self):
    elem = "<{0}".format(self._tag)
    for attribute in self.attributes:
      for key in attribute:
        template = " {0}='{1}'"
        elem += template.format(key, str(attribute[key]))

  def close(self):
    return "</{0}>" % self.tag


class SVGTextNode(SVG):
  def __init__(self, text):
    self._text = text

  @property
  def text(self):
    return self._text

  @text.setter
  def text(self, text):
    self._text = text

  def render(self):
    return self._text


