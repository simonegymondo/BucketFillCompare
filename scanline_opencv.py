from canvas import Canvas
from canvas import timing

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