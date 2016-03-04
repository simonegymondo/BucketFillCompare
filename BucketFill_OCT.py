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


class Canvas(object):
    def __init__(self, pixels):
        self.pixels = pixels

    def __str__(self):
        return '\n'.join(map(lambda row: ''.join(row), self.pixels))

    def fill(self, x, y, color):
        """
        Fills a region of color at a given location with a given color.

        :param x:  the x coordinate where the user clicked
        :param y: the y coordinate where the user clicked
        :param color: the specified color to change the region to
        """
        raise NotImplementedError  # Override this function in the Solution classes


class Solution1(Canvas):
    # TODO write documentation

    def fill(self, x, y, color):
        pass  # TODO write implementation


class Solution2(Canvas):
    # TODO write documentation

    def fill(self, x, y, color):
        pass  # TODO write implementation


def test_solution(impl):
    s = impl([
        ['O', 'X', 'X', 'X', 'X'],
        ['X', 'O', 'O', 'O', 'X'],
        ['X', 'O', '#', 'O', 'X'],
        ['X', 'O', 'O', 'O', 'X'],
        ['X', 'X', 'X', 'X', 'X'],
        ['X', 'X', 'X', '#', '#'],
        ['X', 'X', 'X', 'X', 'X']
    ])
    s.fill(0, 1, '*')
    s.fill(5, 4, 'O')
    s.fill(2, 2, '@')
    assert str(s) == 'O****\n*OOO*\n*O@O*\n*OOO*\n*****\n***OO\n*****'


if __name__ == '__main__':
    test_solution(Solution1)
    test_solution(Solution2)
