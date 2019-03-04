from fact.plotting import camera, mark_pixel
from astropy.io import fits
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

parser = ArgumentParser()
parser.add_argument('inputfile')
parser.add_argument('event', type=int)
parser.add_argument('outputfile')
args = parser.parse_args()

event = args.event


f = fits.open(args.inputfile)

energy = f[1].data['corsika_event_header_total_energy']
photoncharge = f[1].data['photoncharge']
time = f[1].data['arrival_time']
pixels = f[1].data['num_pixel_in_shower']
shower = f[1].data['shower']

# event = np.where(pixels > 50)[0][3]
# event = np.where(energy > 130e3)[0][0]
mask = shower[event]

print(event, energy[event])

fig, (ax1, ax2) = plt.subplots(1, 2)

img = photoncharge[event]
times = (time[event] - time[event][mask].mean()) / 2


d = make_axes_locatable(ax1)
cax = d.append_axes('right', size='5%', pad=0.025)
p = camera(img, cmap='inferno', ax=ax1, vmin=0)
mark_pixel(mask, ax=ax1, color='lightgray', linewidth=0.75)
fig.colorbar(p, cax=cax, label='Photons')


d = make_axes_locatable(ax2)
cax = d.append_axes('right', size='5%', pad=0.025)
p = camera(times, cmap='RdBu_r', ax=ax2, vmin=-10, vmax=10)
fig.colorbar(p, cax=cax, label=r'$(t - \bar{t}) \mathrel{/} \si{\nano\second}$')
mark_pixel(mask, ax=ax2, color='lightgray', linewidth=0.75)

for ax in (ax1, ax2):
    ax.set_axis_off()

fig.tight_layout(pad=0)
fig.savefig(args.outputfile)
