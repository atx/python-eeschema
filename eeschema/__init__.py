# The MIT License (MIT)
# 
# Copyright (c) 2015 Josef Gajdusek
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# TODO: Implement graphic elements
# TODO: Implement loading libraries from files

class SchemaLib:
    """
    SchemaLib() -> new empty SchemaLib
    """

    def __init__(self):
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def to_lib(self):
        ret = "EESchema-LIBRARY Version 2.3\n"
        ret += "#encoding utf-8\n"

        for c in self.components:
            ret += c.to_lib()

        ret += "#End Library\n"
        return ret

    def save(self, fname):
        with open(fname, "w") as f:
            f.write(self.to_lib())


class Component:
    """
    Component(name) -> create new component with name

    Keyword arguments:
    reference -- component reference prefix (default "U")
    drawpinnumber -- display pin numbers (default True)
    drawpinname -- display pin names (default True)
    aliases -- list of aliases to use (default [])
    """

    def __init__(self, name, reference = "U", drawpinnumber = True,
            drawpinname = True, aliases = []):
        self.name = name
        self.reference = reference
        self.drawpinnumber = drawpinnumber
        self.drawpinname = drawpinname
        self.aliases = aliases
        self.fields = {}

        for f in [Field(0, reference), Field(1, name),
                Field(2, "", visible = False), Field(3, "", visible = False)]:
            self.add_field(f)

        self.graphic = []

    def add_field(self, f):
        """add_field(f) -> adds field"""
        self.fields[f.id] = f
        return self

    def add_pin(self, p):
        """add_pin(p) -> adds pin"""
        self.graphic.append(p)
        return self

    def add_graphic(self, p):
        return self.add_pin(p)

    def to_lib(self):
        """Returns this component in KiCad .lib format"""
        ret = "DEF %s %s 0 40 %s %s 1 F N\n" % (self.name, self.reference,
                ("Y" if self.drawpinnumber else "N"),
                ("Y" if self.drawpinname else "N"))
        if self.aliases:
            ret += "ALIAS " + " ".join(self.aliases) + "\n"

        for f in self.fields.values():
            ret += f.to_lib() + "\n"

        ret += "DRAW\n"
        for g in self.graphic:
            ret += g.to_lib() + "\n"
        ret += "ENDDRAW\n"
        ret += "ENDDEF\n"

        return ret


class Field:
    """
    Field(id, text) -> create new Field with id and text

    Keyword arguments:
    x -- x coordinate (default 0)
    y -- y coordinate (default 0)
    dimension -- size (default 50)
    visible -- visibility (default True)
    orientation -- orientation (default Field.HORIZONTAL)
    name -- name (default None)
    hjustify -- text horizontal justify (default LEFT)
    vjustify -- text vertical justify (default CENTER)
    italic -- text italic (default False)
    bold -- text bold (default False)
    """

    HORIZONTAL = "H"
    VERTICAL = "V"

    LEFT = "L"
    RIGHT = "R"
    CENTER = "C"
    BOTTOM = "B"
    TOP = "T"

    def __init__(self, id, text, x = 0, y = 0, dimension = 50, visible = True,
            orientation = HORIZONTAL, name = None, hjustify = LEFT,
            vjustify = CENTER, italic = False, bold = False):
        self.id = id
        self.text = text
        self.x = x
        self.y = y
        self.dimension = dimension
        self.visible = visible
        self.orientation = orientation
        self.hjustify = hjustify
        self.vjustify = vjustify
        self.italic = italic
        self.bold = bold
        self.name = name

    def to_lib(self):
        """Returns this field in KiCad .lib format"""
        return "F%d \"%s\" %d %d %d %s %s %s %s%s%s" % \
                (self.id, self.text, self.x, self.y, self.dimension,
                        self.orientation, ("V" if self.visible else "I"),
                        self.hjustify, self.vjustify,
                        ("I" if self.italic else "N"),
                        ("B" if self.bold else "N"))

class Pin:
    """
    Pin(name, number) -> returns new Pin with name and number

    Note: number does not necessarily have to be int

    Keyword arguments:
    x -- x coordinate (default 0)
    y -- y coordinate (default 0)
    length -- length of the pin line (default 100)
    orientation -- orientation of the pin (default Pin.RIGHT)
    size_num -- size of the pin number (default 50)
    size_name -- size of the pin name (default 50)
    """

    UP = "U"
    DOWN = "D"
    RIGHT = "R"
    LEFT = "L"

    def __init__(self, name, number, x = 0, y = 0, length = 100,
            orientation = RIGHT, size_num = 50, size_name = 50):
        self.name = name
        self.number = number
        self.x = x
        self.y = y
        self.length = length
        self.orientation = orientation
        self.size_num = size_num
        self.size_name = size_name

    def to_lib(self):
        """Returns this pin in KiCad .lib format"""
        return "X %s %s %d %d %d %s %d %d 0 0 I" % \
                (self.name, str(self.number), self.x, self.y, self.length,
                        self.orientation, self.size_num, self.size_name)


class Graphic:

    FG = "F"
    BG = "f"
    NONE = "N"

    def __init__(self, thickness = 0, fill = NONE):
        self.thickness = thickness
        self.fill = fill


class Arc(Graphic):

    def __init__(self, x, y, radius, start_angle, end_angle,
            start_x, start_y, end_x, end_y, thickness = 0, fill = Graphic.NONE):
        super(Arc, self).__init__(thickness = thickness, fill = fill)
        self.x = x
        self.y = y
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    def to_lib(self):
        """Returns this Arc in KiCad .lib format"""
        return "A %d %d %d %d %d 0 1 %d %s %d %d %d %d" % \
                (self.x, self.y, self.radius, self.start_angle, self.end_angle,
                        self.thickness, self.fill, self.start_x, self.start_y,
                        self.end_x, self.end_y)


class Circle(Graphic):

    def __init__(self, x, y, radius, thickness = 0, fill = Graphic.NONE):
        super(Circle, self).__init__(thickness = thickness, fill = fill)
        self.x = x
        self.y = y
        self.radius = radius

    def to_lib(self):
        """Returns this Circle in KiCad .lib format"""
        return "C %d %d %d 0 1 %d %s" % (self.x, self.y, self.radius, self.thickness,
                self.fill)


class Polyline(Graphic):

    def __init__(self, points, thickness = 0, fill = Graphic.NONE):
        super(Polyline, self).__init__(thickness = thickness, fill = fill)
        self.points = points

    def to_lib(self):
        """Returns this Polyline in KiCad .lib format"""
        ret = "P %d 0 1 %d " % (len(self.points), self.thickness)
        for p in self.points:
            ret += "%d %d " % (p[0], p[1])
        ret += "%s" % self.fill
        return ret


class Rectangle(Graphic):

    def __init__(self, start_x, start_y, end_x, end_y, thickness = 0, fill = Graphic.NONE):
        super(Rectangle, self).__init__(thickness = thickness, fill = fill)
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    def to_lib(self):
        """Returns this Rectangle in KiCad .lib format"""
        return "S %d %d %d %d 0 1 %d %s" % (self.start_x, self.start_y,
                self.end_x, self.end_y, self.thickness, self.fill)


class Text(Graphic):

    HORIZONTAL = 0
    VERTICAL = 900

    LEFT = "L"
    RIGHT = "R"
    CENTER = "C"
    BOTTOM = "B"
    TOP = "T"

    def __init__(self, x, y, text, direction = HORIZONTAL, size = 60,
            italic = False, bold = False,
            hjustify = CENTER, vjustify = CENTER):
        self.x = x
        self.y = y
        self.text = text
        self.direction = direction
        self.size = size
        self.bold = bold
        self.italic = italic
        self.hjustify = hjustify
        self.vjustify = vjustify

    def to_lib(self):
        return "T %d %d %d %d 0 0 1 %s %s %s %s %s" % (self.direction, self.x, self.y,
                self.size, self.text.replace(" ", "~"),
                "Italic" if self.italic else "Normal", "0" if self.bold else "1",
                self.hjustify, self.vjustify)
