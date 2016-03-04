# 4-Directions Bucket-Fill Compare
Comparison of some bucket fill algorithms in Python.

This project compares several algorithms for bucket filling. After some investagation 
a subset of 4 meaningful algorithms have been chosen. 

## Testing

The methods have been tested with several test cases and invalid inputs. Also the output
of all bucket filling has been tested against a real image which was bucket filled with GIMP.
All implementations seem to deliver the same image thus prooving correctness.

![Test Image][test_image]

[test_image]: https://github.com/szandara/BucketFillCompare/blob/master/test_kayak_res.jpg

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

# Conclusions

Along with functionality testig, some efficiency measurements were taken. The following
are results average from 10 runs.

### Timing (ms)

| Method         | Recursive  | EdgeSolution  | ScanLineOpenCV | ScanLineWikipedia |
| -------------  |:----------:| -------------:| --------------:| -----------------:|
| test_big_image |0.6091      | 0.28133       | 0.16331        | 0.16188           |
| test_real_image|-           | 37.996        | 18.4931        | 30.6818           |
| test_solution  |0.142       | 0.10113       | 0.100          | 0.1018            |


### Pixel Compare 

| Method         | Recursive  | EdgeSolution  | ScanLineOpenCV | ScanLineWikipedia |
| -------------  |:----------:| -------------:| --------------:| -----------------:|
| test_big_image |1000        | 402           | 304            | 308               |
| test_real_image|-           | 57000         | 28451          | 54671             |
| test_solution  |290         | 290           | 90             | 163               |


We can conclude that the recursive solution is not usable for real scenarios where the image size can grow up to several
thousands of pixel resolutions. That hapens because of the recursion limit which is hit by the algorithm. The problem
can be overcome by increasing the stack size, however that is still not optimal since the timing needed is anyway
higher than the other methods.

The similar edge solution is also quite slow even if it solves the recursion problem. That is due to an increased number of
loops. The Scan Line methods seem to be much more optimal. Among the two, the simple implementation is as fast
as the OpenCV implementation for simple cases, but it deteriorates with the size increase. The scan line implementation
 of OpenCV tend indeed to minimize the array access for pixel comparison giving  advantage in speed especially 
when memory access is expensive or the pixel comparison is non trivial (ie. tolerance filling).
