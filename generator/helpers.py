from functools import partial
from random import randint

d2 = partial(randint, 1, 2)
d4 = partial(randint, 1, 4)
d6 = partial(randint, 1, 6)
d8 = partial(randint, 1, 8)
d10 = partial(randint, 1, 10)
d12 = partial(randint, 1, 12)
d20 = partial(randint, 1, 20)
d100 = partial(randint, 1, 100)
