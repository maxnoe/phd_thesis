import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, PathPatch
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap, to_rgba
from matplotlib.path import Path
import numpy as np
from fact.instrument.camera import get_pixel_dataframe
from shapely.geometry import MultiPolygon, Polygon as ShapelyPolygon
from shapely.ops import cascaded_union
import sys


df = get_pixel_dataframe()
fig, axs = plt.subplots(1, 3)

for ax in axs:
    ax.set_xlim(-195, 195)
    ax.set_ylim(-195, 195)
    ax.set_axis_off()
    ax.set_aspect(1)

pixels = PatchCollection([
    RegularPolygon(xy=(x, y), numVertices=6, radius=9.55 / np.sqrt(3))
    for x, y in zip(df['x'], df['y'])
])
verts = np.array([p.vertices for p in pixels.get_paths()])

colors = []
for i in range(4):
    basecolor = f'C{i}'
    for i in range(10):
        color = list(to_rgba(basecolor))
        color[-1] = (i + 1) / 10
        colors.append(color)
cmap = ListedColormap(colors)


keys = ['CHID', 'bias_patch_id', 'trigger_patch_id']
labels = ['Pixels', 'Bias Patches', 'Trigger Patches']

df.sort_values('CHID', inplace=True)

for ax, key, label in zip(axs, keys, labels):
    ax.set_title(label)
    patches = []
    for patch_id, g in df.groupby(key, sort=False):

        polygons = [ShapelyPolygon(verts[i]) for i in g['CHID']]
        boundary = cascaded_union(polygons)

        if isinstance(boundary, MultiPolygon):
            paths = [
                Path(np.array(polygon.exterior.coords))
                for polygon in boundary
            ]
            path = Path.make_compound_path(*paths, closed=True)
        else:
            path = Path(boundary.exterior.coords, closed=True)

        patch = PathPatch(path)
        patches.append(patch)

    col = PatchCollection(patches)
    col.set_array(np.arange(len(patches)) // (len(patches) / 40))
    col.set_edgecolor('k')
    col.set_linewidth(0.5)
    col.set_cmap(cmap)

    ax.add_collection(col)

fig.tight_layout(pad=0)
fig.savefig(sys.argv[1])
