from canvas import Canvas
from canvas import timing

class ScanlineWikipedia(Canvas):
    """
    This bucket fill solution does not use recursion but it relies on a stack.
    At each iteration the stack is increased with new pixels. The idea is to start
    filling the areas by entire lines (from this, the name), stopping when
    it finds a border pixel (a pixel which does not require filling). While filling
    the line, it also adds to the stack the pixel above and below the beginning of the line.
    This above or beyond pixel is added only when the line scan finds a non fillable pixel,
    this way it ensures that each pixel is only visited once.

    example:

    Iteration 0:

    01234567
    0: OOXXOXXO
    1: OXXXXXOO

    If we start filling from (4,2), the algorithm will start the calculation at (1, 2)
    and will try to fill the whole line. While filling, it will also add (2, 0) and (5, 0)
    to the stack.

    Iteration 1:

    01234567
    0: OOXXOXXO
    1: O*****OO

    Iteration 2:

    01234567
    0: OO**OXXO
    1: O*****OO

    Iteration 3:

    01234567
    0: OO**OXXO
    1: O*****OO

    """
    @timing
    def fill(self, x, y, color):
        self.validate(x, y, color)

        self.max_depth = 0
        old_color = self.pixels[x][y]

        if old_color == color:
            return  # nothing to do

        stack = [(y, x)]
        w = len(self.pixels[0])
        h = len(self.pixels)

        while stack:
            self.max_depth = max(self.max_depth, len(stack))
            cur_point = stack.pop()
            x1, y1 = cur_point

            while x1 >= 0 and self.pixels[y1][x1] == old_color:
                x1 -= 1
            x1 += 1

            above = False
            below = False

            while x1 < w and self.pixels[y1][x1] == old_color:
                self.pixels[y1][x1] = color

                if not above and y1 > 0 and self.pixels[y1 - 1][x1] == old_color:
                    stack.append((x1, y1 - 1))
                    above = True
                elif above and y1 < h - 1 and self.pixels[y1 - 1][x1] != old_color:
                    above = False

                if not below and y1 < h - 1 and self.pixels[y1 + 1][x1] == old_color:
                    stack.append((x1, y1 + 1))
                    below = True
                elif below and y1 < h - 1 and self.pixels[y1 + 1][x1] != old_color:
                    below = False

                x1 += 1

