"""
Bucket Fill Exercise

Imagine you are working on an image editing application. You need to implement a bucket fill tool similar to the one
in paint. The user will use the tool by selecting a color and clicking on the canvas. The tool fills the selected
region of color with the new color.

When a pixel is filled, all of its neighbors (above, below, left, or right) of the same color must also be filled,
as well as their neighbors, and so on, until the entire region has been filled with the new color.

In this exercise, you must write *TWO* implementations of the tool. Each implementation must be different. It is not
required that you invent the solutions yourself. You are encouraged to research the problem. Please write documentation
explaining the difference of each implementation, such as when one solution might be more appropriate than the other.
Don't forget to validate input. There is one existing test, however, you might consider adding some more. Keep in mind
that although the given canvas is small, the solution should be applicable for a real canvas that could have huge
resolutions.

Please use python3 to complete this assignment.
"""
import time
import unittest

timing_count = 0


def timing(f):
    """
    Simple annotation to keep track of the time spent calculating. It's a bit hacky due to the global
    variable but it's a simple solution for this case.
    """
    def wrap(*args):
        global timing_count
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        timing_count += (time2 - time1) * 1000.0
        return ret
    return wrap


class Canvas(object):

    class access_count_array(list):
        """
        Access counter for image matrix.
        """

        def set_parent(self, parent):
            self.parent = parent

        def __getitem__(self, index):
            self.parent.pixel_comparisons += 1
            return list.__getitem__(self, index)

    def __init__(self, pixels):
        self.pixels = Canvas.access_count_array(pixels)
        self.pixels.set_parent(self)
        self.pixel_comparisons = 0

    def __str__(self):
        return '\n'.join(map(lambda row: ''.join(row), self.pixels))

    def validate(self, x, y, color):
        """
        Common validation for the fill input

        :param x:  the x coordinate where the user clicked
        :param y: the y coordinate where the user clicked
        :param color: the specified color to change the region to
        """
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError(
                "Invalid pixel seed format. Expecting integers {},{}".format(
                    x, y))

        if x < 0 or x >= len(self.pixels) \
                or y < 0 or y >= len(self.pixels[0]):
            raise ValueError(
                "Invalid pixel seed for flood fill {},{}".format(
                    x, y))

        try:
            color == self.pixels[x][y]
        except Exception as e:
            raise ValueError("Pixel img and chosen color are of different types: {} and {}"
                             .format(color, self.pixels[x][y]))

    def fill(self, x, y, color):
        """
        Fills a region of color at a given location with a given color.

        :param x:  the x coordinate where the user clicked
        :param y: the y coordinate where the user clicked
        :param color: the specified color to change the region to
        """
        raise NotImplementedError  # Override this function in the Solution classes


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
                    if s >= 0 and s < w and t >= 0 and t < h and self.pixels[
                            s][t] == old_color:
                        self.pixels[s][t] = color
                        newedge.append((s, t))
            edge = newedge


class RecursiveSolution(Canvas):
    """
    This bucket fill solution address the problem using recursion. At each iteration
    all the current neighbours are added to the recursion stack, if the current point
    needs to be filled.
    """

    def _fill(self, x, y, color, old_color):
        h = len(self.pixels[0])
        w = len(self.pixels)

        self.pixel_comparisons += 1
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
                self.pixel_comparisons += 1
                x1 -= 1
            x1 += 1

            above = False
            below = False

            while x1 < w and self.pixels[y1][x1] == old_color:
                self.pixels[y1][x1] = color

                if not above and y1 > 0 and self.pixels[
                        y1 - 1][x1] == old_color:
                    self.pixel_comparisons += 1
                    stack.append((x1, y1 - 1))
                    above = True
                elif above and y1 < h - 1 and self.pixels[y1 - 1][x1] != old_color:
                    self.pixel_comparisons += 1
                    above = False

                if not below and y1 < h - \
                        1 and self.pixels[y1 + 1][x1] == old_color:
                    self.pixel_comparisons += 1
                    stack.append((x1, y1 + 1))
                    below = True
                elif below and y1 < h - 1 and self.pixels[y1 + 1][x1] != old_color:
                    self.pixel_comparisons += 1
                    below = False

                x1 += 1


class ScanlineOpenCV(Canvas):
    """
    This is a scan line approach as designed by OpenCV. The algorithm is similar to
    the scanline as described above but it uses a different flow. Instead of filling
    from left to right, it starts filling from the center to both horizontal directions.
    It maintains a left and right index which are added to the stack and processed
    at each iteration.
    """

    @timing
    def fill(self, x, y, color):
        self.validate(x, y, color)

        old_color = self.pixels[x][y]

        if old_color == color:
            return  # nothing to do

        self.max_depth = 0
        w = len(self.pixels[0])
        h = len(self.pixels)

        l = y
        r = y

        while(r < w and self.pixels[x][r] == old_color):
            self.pixels[x][r] = color
            r += 1

        l -= 1
        while(l >= 0 and self.pixels[x][l] == old_color):
            self.pixels[x][l] = color
            l -= 1

        l += 1
        r -= 1

        stack = [(x, l, r, r + 1, r, 1)]

        while stack:
            self.max_depth = max(self.max_depth, len(stack))
            yc, l, r, pl, pr, dirz = stack.pop()
            data = [[-dirz, l, r], [dirz, l, pl - 1], [dirz, pr + 1, r]]

            for i in range(0, 3):
                dirz = data[i][0]
                yc_d = yc + dirz
                if yc_d >= h or yc_d < 0:
                    continue

                left = data[i][1]
                right = data[i][2]

                k = left

                while k <= right:
                    if k >= 0 and k < w and self.pixels[yc_d][k] == old_color:
                        self.pixels[yc_d][k] = color
                        j = k

                        j -= 1
                        while j >= 0 and self.pixels[yc_d][j] == old_color:
                            self.pixels[yc_d][j] = color
                            j -= 1

                        k += 1
                        while k < w and self.pixels[yc_d][k] == old_color:
                            self.pixels[yc_d][k] = color
                            k += 1

                        stack.append((yc_d, j + 1, k - 1, l, r, -dirz))

                    k += 1


##########################################################################
################################################ TEST CODE ###############

class TestBase():
    """
    This test suit is made to test the floodfill functionalities and it keeps track of timing
    and loop count.
    """

    def setUp(self):
        global timing_count
        timing_count = 0
        self.canvas = None

    def tearDown(self):
        """
        Save run information
        """
        timing_results[
            self.impl][self] = {
            'array_access': self.canvas.pixel_comparisons,
            'timing': timing_count}

    def test_big_image(self):
        """
        Test the behavior on big images
        """
        img = [['O'] * 100] * 100

        self.canvas = self.impl(img)
        self.canvas.fill(0, 1, '*')
        assert all([all(pixel == '*' for pixel in line)
                    for line in self.canvas.pixels])

    def test_is_4_way(self):
        """
        Test that it only support 4-way connection as specified in the test
        """
        self.canvas = self.impl([['O', 'X', 'O'],
                                 ['X', 'O', 'O'],
                                 ['X', 'X', 'X']])

        self.canvas.fill(1, 1, 'X')
        assert str(self.canvas) == 'OXX\nXXX\nXXX'

    def test_fill_same_color(self):
        """
        Test that it only support 4-way connection as specified in the test
        """
        self.canvas = self.impl([['O', 'X', 'O'],
                                 ['X', 'O', 'O'],
                                 ['X', 'X', 'X']])

        self.canvas.fill(1, 0, 'X')
        assert str(self.canvas) == 'OXO\nXOO\nXXX'

    def test_basic_solution(self):
        """
        Test the correct behavior of the method
        """
        self.canvas = self.impl([['O', 'X']])
        self.canvas.fill(0, 1, 'O')
        self.canvas.fill(0, 0, 'O')
        assert str(self.canvas) == 'OO'

    def test_basic_solution_as_array(self):
        """
        Test the correct behavior of the method
        """
        self.canvas = self.impl([['O', 'X', 'O', 'X', 'X', 'X']])
        self.canvas.fill(0, 1, 'O')
        assert str(self.canvas) == 'OOOXXX'

    def test_solution(self):
        """
        Test the correct behavior of the method
        """
        self.canvas = self.impl([
            ['O', 'X', 'X', 'X', 'X'],
            ['X', 'O', 'O', 'O', 'X'],
            ['X', 'O', '#', 'O', 'X'],
            ['X', 'O', 'O', 'O', 'X'],
            ['X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', '#', '#'],
            ['X', 'X', 'X', 'X', 'X'],
        ])
        self.canvas.fill(0, 1, '*')
        self.canvas.fill(5, 4, 'O')
        self.canvas.fill(2, 2, '@')
        assert str(
            self.canvas) == 'O****\n*OOO*\n*O@O*\n*OOO*\n*****\n***OO\n*****'

    def test_real_image(self):
        """
        Test with real data using a preprocessed and floodfilled Gimp image
        as ground truth.
        """
        try:
            import numpy
        except ImportError as e:
            return

        from PIL import Image
        with Image.open('test_kayak.bmp').convert('RGB') as image:
            img = numpy.array(image)

            self.canvas = self.impl(img[:, :, 0])
            self.canvas.fill(1038, 399, 0)

        with Image.open('test_kayak_res.bmp').convert('RGB') as res_image:
            img_test = numpy.array(self.canvas.pixels)
            img_res = numpy.array(res_image)[:, :, 0]
            assert 0 == numpy.sum(img_test - img_res)

    def test_out_of_bound_seed(self):
        """
        Test corner cases
        """
        with self.assertRaises(ValueError):
            self.canvas = self.impl([[0, 0], [0, 1]])
            self.canvas.fill(1292, 956, 12)

    def test_wrong_seed(self):
        """
        Test corner cases
        """
        with self.assertRaises(ValueError):
            self.canvas = self.impl([[0, 0], [0, 1]])
            self.canvas.fill('a', 956, 12)

    def test_wrong_input(self):
        """
        Test corner cases
        """
        with self.assertRaises(ValueError):
            self.canvas = self.impl([])
            self.canvas.fill(1038, 399, 12)

    def test_wrong_input(self):
        """
        Test corner cases
        """
        with self.assertRaises(ValueError):
            self.canvas = self.impl([[0, 0], [0, 1]])
            self.canvas.fill(1292, 956, 'a')


timing_results = {RecursiveSolution: {},
                  ScanlineOpenCV: {},
                  ScanlineWikipedia: {},
                  EdgeSolution: {}
                  }


class TestRecursive(TestBase, unittest.TestCase):
    """
    Test suite for Recursive solution
    """
    impl = RecursiveSolution


class TestScanlineOpenCV(TestBase, unittest.TestCase):
    """
    Test suite for Scanline OpenCV version
    """
    impl = ScanlineOpenCV


class TestScanlineWikipedia(TestBase, unittest.TestCase):
    """
    Test suite for Scanline wikipedia version
    """
    impl = ScanlineWikipedia


class TestEdgeSolution(TestBase, unittest.TestCase):
    """
    Test suite for EdgeSolution
    """
    impl = EdgeSolution

if __name__ == '__main__':
    unittest.main(exit=False)
    print(timing_results)
