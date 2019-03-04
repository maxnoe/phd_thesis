# phd_thesis


## Software

To build my thesis, you will need:

1. The python packages defined in environment.yaml.
  Create a new conda environment using:
  ```
  $ conda env create -n phd_maxnoe -f environment.yaml
  $ conda activate phd_maxnoe
  ```

2. TeXLive 2020

3. make

4. the input data


## Input data

All input files to produce the final plots in the thesis are stored
on the storage server `big-tank.app.tu-dortmund.de` in `/POOL/users/mnoethe/phd_thesis`.

These are the higher level analysis results (so after FACT-Tools processing), as
the Raw Data would be to much to download to a single machine and do the processing.


Link that storage locationto `data` in the root of this repository, e.g. by
using `ln -s /net/big-tank/POOL/users/mnoethe/phd_thesis data` or by using `sshfs`
or just downloading the data.


## Final PDF/A document


Unfortunately, I was unable to produce a fully PDF/A-3u compatible document
out of matplotlib/pgfplots/lualatex.

As a final step, a conversion using Adobe Acrobat DC was done,
this fixed the one remaining issue, namely the `/Interpolate true` setting for images.
