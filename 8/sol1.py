#!/usr/bin/env python3

import numpy as np

data = [int(x) for x in list(open('input').read().strip('\n'))]
data = np.array(data).reshape(-1, 6, 25)
fewest_zeros = np.argmin(np.count_nonzero(data == 0, axis=(1, 2)))
layer = data[fewest_zeros, :, :]
print((layer == 1).sum() * (layer == 2).sum())
