from canvas import Canvas
from canvas import timing

class RecursiveSolution(Canvas):
    """
    This bucket fill solution address the problem using recursion. At each iteration
    all the current neighbours are added to the recursion stack, if the current point
    needs to be filled.
    """

    def _fill(self, x, y, color, old_color):
        """
        Support recursive method.
        """
        h = len(self.pixels[0])
        w = len(self.pixels)

        if self.pixels[x][y] == old_color:
            self.pixels[x][y] = color

            if x > 0:
                self._fill(x - 1, y, color, old_color)  # left
            if x < w - 1:
                self._fill(x + 1, y, color, old_color)  # right
            if y > 0:
                self._fill(x, y - 1, color, old_color)  # up
            if y < h - 1:
                self._fill(x, y + 1, color, old_color)  # down

    @timing
    def fill(self, x, y, color):
        self.validate(x, y, color)
        old_color = self.pixels[x][y]

        if old_color == color:
            return  # nothing to do

        try:
            self._fill(x, y, color, old_color)
        except RuntimeError as e:
            print("Overflow reached")
