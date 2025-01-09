#import numpy as np

#import pdb
#from color import Color


def decide(P):
    p_1 = P[0]
    p_2 = P[1]
    p_3 = P[2]
    p_4 = P[3]

    x_target = (p_2[0] + p_1[0]) / 2
    z_target = (p_2[1] + p_1[1]) / 2

    return(x_target, z_target)