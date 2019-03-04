import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u
from scipy.fftpack import irfft
from ctapipe.visualization import CameraDisplay
from ctapipe.instrument import CameraGeometry
from ctapipe.coordinates import EngineeringCameraFrame
from ctapipe.image.toymodel import SkewedGaussian
from ctapipe.image.hillas import camera_to_shower_coordinates
from ctapipe.image import tailcuts_clean

np.random.seed(0)


def sig(x, x0, a):
    return 1 / (1 + np.exp(-a * (x - x0)))


def pulse(x, A, t0, t1, a, b):
    sig1 = sig(x, t0, a)
    sig2 = 1 - sig(x, t1, b)
    return A * sig1 * sig2


def pink_noise(N, noise, amplitude):
    f = np.arange(1, N + 1)
    power = 1 / f
    power += np.random.normal(0, noise * power)
    noise = irfft(power)
    return (noise - noise.mean()) * amplitude / noise.max()


pixels = []
for mean, amplitude in zip((15, 20), (5, 10)):
    x = np.arange(0, 60.1, 0.5)
    p = pulse(x, amplitude, mean, mean + 5, 2, 0.25)
    noise = pink_noise(len(x), 3, 1)
    pixels.append((p, noise))


fig = plt.figure(figsize=(3, 2), constrained_layout=True)
ax = fig.add_subplot(1, 1, 1)
ax.set_axis_off()

for pix, (p, noise) in zip((42, 314), pixels):
    ax.plot(x, ((p + noise + 0.5) * 2**16).astype(int), label=f'Pixel {pix}')

ax.legend(loc=(0.5, 0.6), frameon=False)

fig.savefig('build/raw_data.pdf')


fig = plt.figure(figsize=(3, 2), constrained_layout=True)
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('time / ns')
ax.set_axis_off()

for pix, (p, noise) in zip((42, 314), pixels):
    ax.plot(x, p + 0.2 * noise, label=f'Pixel {pix}')

ax.legend(loc=(0.5, 0.6), frameon=False)

fig.savefig('build/calibrated.pdf')


hillas = dict(
    x=80 * u.mm, y=20 * u.mm,
    width=15 * u.mm, length=50 * u.mm,
    psi=35 * u.deg,
)


cam = CameraGeometry.from_name('FACT').transform_to(EngineeringCameraFrame())
longi, trans = camera_to_shower_coordinates(
    cam.pix_x, cam.pix_y, hillas['x'], hillas['y'], hillas['psi']
)


m = SkewedGaussian(**hillas, skewness=0.3)
img, signal, noise = m.generate_image(cam, intensity=2500, nsb_level_pe=3)

time_noise = np.random.uniform(0, 60, cam.n_pixels)
time_image = 0.2 * longi.to_value(u.mm) + 25

time = np.average(
    np.column_stack([time_noise, time_image]),
    weights=np.column_stack([noise, signal]) + 1,
    axis=1
)

inferno = plt.get_cmap('inferno')
inferno.set_bad('gray')
rdbu = plt.get_cmap('RdBu_r')
rdbu.set_bad('gray')


for i in range(2):
    fig, axs = plt.subplots(1, 2, figsize=(5, 2), constrained_layout=True)

    if i == 1:
        clean = tailcuts_clean(cam, img, 9, 3)
        img[~clean] = np.nan
        time[~clean] = np.nan

    disp = CameraDisplay(cam, ax=axs[0])
    disp.image = img
    disp.cmap = inferno
    disp.add_colorbar(ax=axs[0])
    disp.set_limits_minmax(0, 45)
    disp.pixels.set_rasterized(True)

    disp2 = CameraDisplay(cam, ax=axs[1])
    disp2.image = time
    disp2.cmap = rdbu
    disp2.set_limits_minmax(10, 40)
    disp2.add_colorbar(ax=axs[1])
    disp2.pixels.set_rasterized(True)

    axs[0].set_title('\# Photons')
    axs[1].set_title('Time / ns')

    for ax in axs:
        ax.set_axis_off()
        ax.set_aspect(1, 'box')
        ax.set_xlim(-0.192, 0.192)
        ax.set_ylim(-0.19, 0.19)

    fig.savefig(f'build/camera_image_{i}.pdf')
