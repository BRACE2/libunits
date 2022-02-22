import numpy as onp
import jax.numpy as jnp

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from .simple import TC_Sect


def surface_points(Qm, fy=1.0, yref=0.0, norm=False, scale=None, **kwds):
    to_float = True
    nIP = len(Qm[0])

    f_n = [
        [fy * (-1) ** (j > i) for i in range(1, nIP + 1)] for j in range(1, nIP + 1)
    ] + [[fy * (-1) ** (j < i) for i in range(1, nIP + 1)] for j in range(0, nIP)]

    N, M = [], []
    for f in f_n:
        sri = Qm @ f
        N.append(sri[0])
        M.append(sri[1])
    N.append(N[0])
    M.append(M[0])

    if norm:
        if scale is None:
            Np_pos = N[0]
            Np_neg = N[nIP]

            Mp_pos = M[nIP * 3 // 2]
            Mp_neg = M[nIP // 2]
        else:
            Np_pos = scale[1]
            Np_neg = -Np_pos
            Mp_pos = scale[0]
            Mp_neg = -Mp_pos

        M[0:nIP] = [-Mi / Mp_neg for Mi in M[0:nIP]]
        M[nIP:] = [Mi / Mp_pos for Mi in M[nIP:]]

        N[0 : nIP // 2] = [Ni / Np_pos for Ni in N[0 : nIP // 2]]
        N[nIP // 2 : nIP * 3 // 2 + 1] = [
            -Ni / Np_neg for Ni in N[nIP // 2 : nIP * 3 // 2 + 1]
        ]

        N[nIP * 3 // 2 :] = [Ni / Np_pos for Ni in N[nIP * 3 // 2 :]]

    if to_float:
        N = [float(Ni) for Ni in N]
        M = [float(Mi) for Mi in M]

    return M, N


def plot_strain(yi, e, ax=None, mpl={}, x_scale=1.0, **kwds):
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig, ax = ax

    epsi = []

    def eps(y, epsa, kappa):
        return epsa - y * kappa

    for i, y in enumerate(yi):
        epsi.append(eps(y, *e) * x_scale)
    #         ax.annotate(round(epsi[i],4),(epsi[i], y*0.99))

    ax.plot(epsi, yi)
    #     ax.fill_betweenx(yi,epsi,0.,alpha=0.2)
    ax.axhline(y=0, color="k")
    ax.axvline(x=0, color="k")
    return fig, ax


def plot_stress(yi, sigi, ax=None, mpl={}, x_scale=1.0):
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig, ax = ax

    sigi = [sig * x_scale for sig in sigi]

    #     for i,y in enumerate(yi):
    #         ax.annotate(round(sigi[i],4),(sigi[i], y*1.01))

    ax.plot(sigi, yi)
    #     ax.fill_betweenx(yi,sigi,0.,alpha=0.2)

    ax.axhline(y=0, color="k")
    ax.axvline(x=0, color="k")
    return fig, ax


def plot_surface(nIP, dA, yi, MatData, ax=None, mpl={}, norm=True, scale=None, **kwds):

    M, N = surface_points(nIP, dA, yi, MatData, norm, scale)

    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig, ax = ax

    ax.plot(M, N, **mpl)
    #     ax.grid(linestyle=':')
    ax.axhline(y=0, color="k")
    ax.axvline(x=0, color="k")
    return fig, ax


def My_abd(k, yref, ymf, d, bf, tf, tw, fy, E):
    r"""
    Yield moment

    $M_u(\kappa) = -\int _c^{d-h}\left(f-Ek\left(x+h\right)\right)xdx = -\frac{-2d^3Ek+2c^3Ek-Ekh^3+3d^2Ekh+3c^2Ekh+3d^2f-3c^2f+3fh^2-6dfh}{6}$

    $M_b = -\int _{-h}^{d-h}\left(f-Ek\left(x+h\right)\right)xdx = -\frac{-2d^3Ek+3d^2Ekh+3d^2f-6dfh}{6}$

    """
    h = d / 2 + yref
    c = (ymf - yref) - tf / 2
    assert ymf + d / 2 + tf / 2 == d
    Mu = -(bf - tw) * (
        (
            -6 * d * fy * h
            + 3 * (fy * h ** 2)
            - 3 * c ** 2 * fy
            + 3 * (d ** 2 * fy)
            + 3 * (c ** 2 * (E * (h * k)))
            + 3 * (d ** 2 * (E * (h * k)))
            - E * h ** 3 * k
            + 2 * (c ** 3 * (E * k))
            - 2 * d ** 3 * (E * k)
        )
        / 6
    )
    Mb = (
        -tw
        * (
            -6 * d * fy * h
            + 3 * (d ** 2 * fy)
            + 3 * (d ** 2 * (E * (h * k)))
            - 2 * d ** 3 * (E * k)
        )
        / 6
    )
    return Mu + Mb


def Ny_abd(k, yref, ymf, d, bf, tf, tw, fy, E):
    """

    N_b(\kappa,h) = b_b \int _{-h}^{d-h} f_y - E k \left(x+h\right)dx = b_b (d f_y-\kappa E\left(h d+\frac{\left(-h+d\right)^2}{2}-\frac{h^2}{2}\right))

    N_u(\kappa,h) = b_u \int _c^{d-h}    f_y - E k \left(x+h\right)dx = b_u (f_y\left(-h+d\right)-f_y c-\kappa E\left(h\left(-h+d\right)-hc+\frac{\left(-h+d\right)^2}{2}-\frac{c^2}{2}\right))

    """
    h = d / 2 + yref
    c = (ymf - yref) - tf / 2
    assert ymf + d / 2 + tf / 2 == d

    Nb = tw * (d * fy - k * E * (-(h ** 2) / 2 + d * h + (d - h) ** 2 / 2))
    Nu = (bf - tw) * (
        -k * E * (-(c ** 2) / 2 + (d - h) ** 2 / 2 - c * h + h * (d - h))
        - c * fy
        + fy * (d - h)
    )
    return Nb + Nu


def yield_points(yref, ymf, d, bf, tw, fy, E, **kwds):
    n_abd = 10
    tf = 2 * (d / 2 - ymf)

    kap = onp.linspace(0.0, 2.0 * fy / E / d, n_abd)

    N = [Ny_abd(kap[i], yref, ymf, d, bf, tf, tw, fy, E) for i in range(n_abd)]
    M = [My_abd(kap[i], yref, ymf, d, bf, tf, tw, fy, E) for i in range(n_abd)]

    N.extend([-Ny_abd(kap[i], yref, ymf, d, bf, tf, tw, fy, E) for i in range(n_abd)])
    M.extend([-My_abd(kap[i], yref, ymf, d, bf, tf, tw, fy, E) for i in range(n_abd)])

    N.append(N[0])
    M.append(M[0])

    return M, N


def plastic_points(Qm, fy, yref=0.0, norm=False, scale=None, **kwds):
    to_float = True
    nIP = len(Qm[0, :])
    f_n = [
        [fy * (-1) ** (j > i) for i in range(1, nIP + 1)] for j in range(1, nIP + 1)
    ] + [[fy * (-1) ** (j < i) for i in range(1, nIP + 1)] for j in range(0, nIP)]

    N, M = [], []
    for f in f_n:
        sri = Qm @ f
        N.append(sri[0])
        M.append(sri[1])
    N.append(N[0])
    M.append(M[0])
    if norm:
        if scale is None:
            Np_pos = N[0]
            Np_neg = N[nIP]

            Mp_pos = M[nIP * 3 // 2]
            Mp_neg = M[nIP // 2]
        else:
            Np_pos = scale[1]
            Np_neg = -Np_pos
            Mp_pos = scale[0]
            Mp_neg = -Mp_pos

        M[0:nIP] = [-Mi / Mp_neg for Mi in M[0:nIP]]
        M[nIP:] = [Mi / Mp_pos for Mi in M[nIP:]]

        N[0 : nIP // 2] = [Ni / Np_pos for Ni in N[0 : nIP // 2]]
        N[nIP // 2 : nIP * 3 // 2 + 1] = [
            -Ni / Np_neg for Ni in N[nIP // 2 : nIP * 3 // 2 + 1]
        ]

        N[nIP * 3 // 2 :] = [Ni / Np_pos for Ni in N[nIP * 3 // 2 :]]

    if to_float:
        N = [float(Ni) for Ni in N]
        M = [float(Mi) for Mi in M]
    return M, N


def plot_surface_T(yref, ymf, d, bf, tw, fy, E, quad, ax=None, mpl={}):
    tf = 2 * (d / 2 - ymf)

    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig, ax = ax

    SectData = TC_Sect(d, bf, tw, quad, yref, ymf=ymf)
    # print(SectData)
    Qm = SectData["Qm"]

    Mp, Np = plastic_points(Qm, fy, yref=0.0, norm=False, scale=None)

    My, Ny = yield_points(yref, ymf, d, bf, tw, fy, E)

    plastic_surface = ax.plot(Mp, Np, label="p")[0]
    yield_surface = ax.plot(My, Ny, "r", ":", label="y")[0]

    return plastic_surface, yield_surface
