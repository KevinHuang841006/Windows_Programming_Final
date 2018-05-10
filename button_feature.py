import numpy as np

def set_flag(tooth_flag):
    print(tooth_flag)
    np.save('flag.npy',tooth_flag)
    
