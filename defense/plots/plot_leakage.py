from ctapipe.visualization import CameraDisplay
from ctapipe.instrument import CameraGeometry
from ctapipe.coordinates import EngineeringCameraFrame
from ctapipe.image.toymodel import SkewedGaussian
import matplotlib.pyplot as plt
import astropy.units as u
import numpy as np

np.random.seed(1337)


geom = CameraGeometry.from_name('FACT')
geom = geom.transform_to(EngineeringCameraFrame())
model = SkewedGaussian(
    width=0.01 * u.m, length=0.03 * u.m,
    x=0.14 * u.m, y=0.07 * u.m,
    skewness=0.05, psi=30 * u.deg,
)
img, signal, noise = model.generate_image(geom, 1000, nsb_level_pe=2)


fig = plt.figure(figsize=(5, 5))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_axis_off()

disp = CameraDisplay(geom, image=img, ax=ax, cmap='inferno')
disp.highlight_pixels(geom.get_border_pixel_mask(2), color='C0')
ax.set_title('')

fig.savefig('build/leakage.pdf', bbox_inches='tight')
