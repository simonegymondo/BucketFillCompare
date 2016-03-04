from canvas import Canvas
from canvas import timing

class EdgeSolution(Canvas):
    """
    This is similar to the RecursiveSolution except it uses a queue to avoid
    recursion. The flooding type is breadth first since it tries to expand
    from the starting point out to the edges.
    """
    @timing
    def fill(self, x, y, color):
        self.validate(x, y, color)
        h = len(self.pixels[0])
        w = len(self.pixels)
        old_color = self.pixels[x][y]

        if old_color == color:
            return

        edge = [(x, y)]
        self.pixels[x][y] = color
        while edge:
            newedge = []
            for (x, y) in edge:
                for (s, t) in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= s < w and 0 <= t < h and self.pixels[s][t] == old_color:
                        self.pixels[s][t] = color
                        newedge.append((s, t))
            edge = newedge
