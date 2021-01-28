"""
Contains different utility during data processing


"""
import numpy as np



def generate_color(number):
    color = '#{:02x}{:02x}{:02x}'.format(*map(lambda x: np.random.randint(0, 255), range(3)))
    g=np.array([generate_color() for var in range(1000)])
    colors=g[np.random.randint(number,size=npber)]
    return colors

