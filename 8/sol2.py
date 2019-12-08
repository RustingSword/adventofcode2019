#!/usr/bin/env python3.7

import numpy as np

data = [int(x) for x in list(open('input').read().strip('\n'))]
data = np.array(data).reshape(-1, 6, 25)
idx = np.expand_dims(np.argmax(data != 2, axis=0), axis=0)
res = np.squeeze(np.take_along_axis(data, idx, axis=0))

msg = []
for line in res:
    msg.extend(list(map(lambda x: '1' if x == 1 else ' ', line)))
    msg.append('\n')
print(''.join(msg))
