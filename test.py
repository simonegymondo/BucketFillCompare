"""
Test class for bucket fill.
"""
from recursive import RecursiveSolution
from scanline_opencv import ScanlineOpenCV
from scanline_wikipedia import ScanlineWikipedia
from edge import EdgeSolution
from canvas import timing_count
import unittest

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
        method_name = self.id().split('.')[-1]
        timing_results[self.impl][method_name] = {
            'array_access': self.canvas.pixel_comparisons,
            'timing': self.canvas.timing_count}

    def test_big_image(self):
        """
        Test the behavior on big images
        """
        img = [['O'] * 100] * 100

        self.canvas = self.impl(img)
        self.canvas.fill(0, 1, '*')
        self.assertTrue(all([all(pixel == '*' for pixel in line)
                    for line in self.canvas.pixels]))

    def test_is_4_way(self):
        """
        Test that it only support 4-way connection as specified in the test
        """
        self.canvas = self.impl([['O', 'X', 'O'],
                                 ['X', 'O', 'O'],
                                 ['X', 'X', 'X']])

        self.canvas.fill(1, 1, 'X')
        self.assertTrue(str(self.canvas) == 'OXX\nXXX\nXXX')

    def test_fill_same_color(self):
        """
        Test that it only support 4-way connection as specified in the test
        """
        self.canvas = self.impl([['O', 'X', 'O'],
                                 ['X', 'O', 'O'],
                                 ['X', 'X', 'X']])

        self.canvas.fill(1, 0, 'X')
        self.assertTrue(str(self.canvas) == 'OXO\nXOO\nXXX')

    def test_basic_solution(self):
        """
        Test the correct behavior of the method
        """
        self.canvas = self.impl([['O', 'X']])
        self.canvas.fill(0, 1, 'O')
        self.canvas.fill(0, 0, 'O')
        self.assertTrue(str(self.canvas) == 'OO')

    def test_basic_solution_2lines(self):
        """
        Test the correct behavior of the method
        """
        self.canvas = self.impl([['O', 'X'],['O', 'X']])

        self.canvas.fill(0, 1, 'O')
        self.canvas.fill(0, 0, 'O')

        self.assertTrue(str(self.canvas) == 'OO\nOO')

    def test_basic_solution_as_array(self):
        """
        Test the correct behavior of the method
        """
        self.canvas = self.impl([['O', 'X', 'O', 'X', 'X', 'X']])
        self.canvas.fill(0, 1, 'O')
        self.assertTrue(str(self.canvas) == 'OOOXXX')

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
        self.assertTrue(str(self.canvas) == 'O****\n*OOO*\n*O@O*\n*OOO*\n*****\n***OO\n*****')

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
            self.assertTrue(0 == numpy.sum(img_test - img_res))

    def test_out_of_bound_seed(self):
        """
        Test corner cases
        """
        with self.assertRaises(ValueError):
            self.canvas = self.impl([[0, 0], [0, 1]])
            self.canvas.fill(1292, 0, 12)

    def test_wrong_seed(self):
        """
        Test corner cases
        """
        with self.assertRaises(ValueError):
            self.canvas = self.impl([[0, 0], [0, 1]])
            self.canvas.fill('a', 0, 12)

    def test_wrong_input(self):
        """
        Test corner cases
        """
        with self.assertRaises(ValueError):
            self.canvas = self.impl([])
            self.canvas.fill(0, 0, 12)

    def test_input_different_types(self):
        """
        Test corner cases
        """
        self.canvas = self.impl([[0, 0], [0, 1]])
        self.canvas.fill(0, 0, 'a')
        self.assertTrue(str(self.canvas) == 'aa\na1')

    def test_inconsistent_dims_input(self):
        """
        Test corner cases
        """
        with self.assertRaises(ValueError):
            self.canvas = self.impl([[0, 0], [1]])
            self.canvas.fill(0, 0, 'a')


    def test_inconsistent_dims_input(self):
        """
        Test corner cases
        """
        with self.assertRaises(ValueError):
            self.canvas = self.impl([['a', 0], [1]])
            self.canvas.fill(0, 0, 'a')

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

    """
    # This code is used to print out some nice result.
    
    test_timing = {}
    test_access = {}
    import pprint
    
    for method, test_run in timing_results.items():
        method = method.__name__.split('.')[-1]
        for k,v in test_run.items():
            if k not in test_timing:
                test_timing[k] = {}
            test_timing[k][method] = v['timing']
            
            if k not in test_access:
                test_access[k] = {}
            test_access[k][method] = v['array_access']
            
            
    pprint.pprint(test_timing)
    pprint.pprint(test_access)
    """
