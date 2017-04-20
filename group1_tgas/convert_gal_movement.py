import numpy as np


def gal_uvw(ra, dec, pmra, pmdec, vrad, plx, lsr=False):
    cosd = np.cos(np.deg2rad(dec))
    sind = np.sin(np.deg2rad(dec))
    cosa = np.cos(np.deg2rad(ra))
    sina = np.sin(np.deg2rad(ra))

    k = 4.74047   # Equivalent of 1 A.U/yr in km/s

    A_G = [[0.0548755604, +0.4941094279, -0.8676661490],
           [0.8734370902, -0.4448296300, -0.1980763734],
           [0.4838350155, +0.7469822445, +0.4559837762]]

    vec1 = vrad
    vec2 = k * pmra / plx
    vec3 = k * pmdec / plx

    u = ((A_G[0][0] * cosa * cosd + A_G[1][0] * sina * cosd + A_G[2][0] * sind) * vec1 +
         (-A_G[0][0] * sina + A_G[1][0] * cosa) * vec2 +
         (-A_G[0][0] * cosa * sind - A_G[1][0] * sina * sind + A_G[2][0] * cosd) * vec3)

    v = ((A_G[0][1] * cosa * cosd + A_G[1][1] * sina * cosd + A_G[2][1] * sind) * vec1 +
         (-A_G[0][1] * sina + A_G[1][1] * cosa) * vec2 +
         (-A_G[0][1] * cosa * sind - A_G[1][1] * sina * sind + A_G[2][1] * cosd) * vec3)

    w = ((A_G[0][2] * cosa * cosd + A_G[1][2] * sina * cosd + A_G[2][2] * sind) * vec1 +
         (-A_G[0][2] * sina + A_G[1][2] * cosa) * vec2 +
         (-A_G[0][2] * cosa * sind - A_G[1][2] * sina * sind + A_G[2][2] * cosd) * vec3)

    lsr_vel = np.array([-8.5, 13.38, 6.49])

    if lsr:
        u += lsr_vel[0]
        v += lsr_vel[1]
        w += lsr_vel[2]

    return u, v, w
    # return np.hstack((u, v, w))  # units are km/s
