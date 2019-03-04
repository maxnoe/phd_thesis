import numpy as np
from scipy.stats import norm, skewnorm
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output')
args = parser.parse_args()

np.random.seed(42)


def generate_shower(cog_x, cog_y, width, length, size, delta, skewness):

    photons_long = skewnorm(skewness, 0, length).rvs(size)
    photons_trans = norm(0, width).rvs(size)

    photons_x = np.cos(delta) * photons_long + np.sin(delta) * photons_trans
    photons_y = - np.sin(delta) * photons_long + np.cos(delta) * photons_trans

    photons_x += cog_x
    photons_y += cog_y

    return photons_x, photons_y, photons_long, photons_trans


def calc_hillas(photon_x, photon_y):

    cog_x = np.mean(photon_x)
    cog_y = np.mean(photon_y)

    cov = np.cov(photon_x, photon_y)

    eig_vals, eig_vecs = np.linalg.eigh(cov)

    width, length = np.sqrt(eig_vals)

    delta = np.arctan(eig_vecs[1, 1] / eig_vecs[1, 0])

    return cog_x, cog_y, width, length, delta


def xy2lt(x, y, cog_x, cog_y, delta):
    l = np.cos(delta) * (x - cog_x) + np.sin(delta) * (y - cog_y)
    t = -np.sin(delta) * (x - cog_x) + np.cos(delta) * (y - cog_y)
    return l, t


width = 10
length = 35
cog_x = 100
cog_y = 100
delta = np.deg2rad(-40)
size = 500

px, py, pl, pt = generate_shower(
    cog_x=cog_x,
    cog_y=cog_y,
    width=width,
    length=length,
    size=size,
    delta=delta,
    skewness=2,
)

cog_x, cog_y, width, length, delta = calc_hillas(px, py)

l, t = xy2lt(px, py, cog_x, cog_y, delta)


plot_width = 0.75
plot_height = width / length * plot_width
xmargin = 0.15
ymargin = 0.1


fig = plt.figure()

ax = fig.add_axes([xmargin, ymargin, plot_width, plot_height])

ax_l = fig.add_axes([xmargin, plot_height + ymargin, plot_width, 1 - plot_width], sharex=ax)
ax_t = fig.add_axes([plot_width + xmargin, ymargin, 1 - plot_width - xmargin, plot_height], sharey=ax)

ax.set_xlim(-3 * length, 3 * length)
ax.set_ylim(-3 * width, 3 * width)

ax_l.set_xlim(-3 * length, 3 * length)
ax_l.set_ylim(0, 0.025)

ax_t.set_xlim(0, 0.045)
ax_t.set_ylim(-3 * width, 3 * width)

ax_l.set_axis_off()
ax_t.set_axis_off()


ax.set_xticks(np.arange(-3 * length, 3.1 * length, length))
ax.set_yticks(np.arange(-3 * width, 3.1 * width, width))

ax.set_xticklabels([r'${} \cdot l$'.format(i) for i in range(-3, 4)])
ax.set_yticklabels([r'${} \cdot w$'.format(i) for i in range(-3, 4)])


x, y = np.meshgrid(
    np.linspace(-3 * length, 3 * length, 100),
    np.linspace(-3 * width, 3 * width, 100)
)


kernel = gaussian_kde([l, t])

values = kernel([x.ravel(), y.ravel()]).reshape(x.shape)


ax.contourf(
    x, y,
    values,
    cmap='inferno',
)

x = np.linspace(-3 * length, 3 * length, 100)

ax_l.plot(x, gaussian_kde(l)(x))
ax_l.plot(x, norm.pdf(x, 0, length), 'k--')
ax_l.annotate(
    'Normalverteilung',
    (length, norm.pdf(length, 0, length)),
    (10, 20), textcoords='offset points',
    va='bottom',
    ha='center',
    arrowprops=dict(
        facecolor='k',
        headwidth=3,
        width=0.25,
        headlength=2,
        shrink=0.1,
    ),
)

x = np.linspace(-3 * width, 3 * width, 100)
ax_t.plot(gaussian_kde(t)(x), x)
ax_t.plot(norm.pdf(x, 0, width), x, 'k--')

if args.output:
    plt.savefig(args.output, dpi=300, bbox_inches='tight')
