# BucketFillCompare
Comparison of some bucket fill algorithms in Python.

This project compares several algorithms for bucket filling. After some investagation 
a subset of 4 meaningful algorithms have been chosen. 

## Recursive Solution
This is a scan line approach as designed by OpenCV. The algorithm is similar to
the scanline as described above but it uses a different flow. Instead of filling
from left to right, it starts filling from the center to both horizontal directions.
It maintains a left and right index which are added to the stack and processed
at each iteration.

## Scanline horizontal

This bucket fill solution does not use recursion but it relies on a stack.
At each iteration the stack is increased with new pixels. The idea is to start
filling the areas by entire lines (from this, the name), stopping when
it finds a border pixel (a pixel which does not require filling). While filling
the line, it also adds to the stack the pixel above and below the beginning of the line.
This above or beyond pixel is added only when the line scan finds a non fillable pixel,
this way it ensures that each pixel is only visited once.

## Scanline OpenCV
This is a scan line approach as designed by OpenCV. The algorithm is similar to
the scanline as described above but it uses a different flow. Instead of filling
from left to right, it starts filling from the center to both horizontal directions.
It maintains a left and right index which are added to the stack and processed
at each iteration.

## Edge Solution (Non recursive)
This is similar to the RecursiveSolution except it uses a queue to avoid
recursion. The flooding type is breadth first since it tries to expand
from the starting point out to the edges.

Conclusions

Along with functionality testig, some efficiency measurements were taken.

 'test_big_image': {'EdgeSolution': 0.28133392333984375,
                    'RecursiveSolution': 0.6091594696044922,
                    'ScanlineOpenCV': 0.1633167266845703,
                    'ScanlineWikipedia': 0.16188621520996094},
 'test_real_image': {'EdgeSolution': 37.99629211425781,
                     'RecursiveSolution': 4.969120025634766,
                     'ScanlineOpenCV': 18.491506576538086,
                     'ScanlineWikipedia': 30.68375587463379},
 'test_solution': {'EdgeSolution': 0.10180473327636719,
                   'RecursiveSolution': 0.14281272888183594,
                   'ScanlineOpenCV': 0.10085105895996094,
                   'ScanlineWikipedia': 0.10323524475097656},
