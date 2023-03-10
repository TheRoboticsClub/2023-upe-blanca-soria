from GUI import GUI
from HAL import HAL
# Enter sequential code!
v=0
w=0.2
inc=0.001
while True:
    # Enter iterative code!
    v = v + inc
    HAL.setV(v)
    HAL.setW(w)