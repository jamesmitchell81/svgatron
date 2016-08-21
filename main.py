from svg import SVGElement, SVGRoot
from props import Props

def main():

  root = SVGRoot()
  elem = SVGElement("d")
  root.addElement(elem)

  elem.addAttribute("width", 10)

  print root.render()

if __name__ == "__main__":
  main()
