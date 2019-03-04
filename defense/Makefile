all: build/phd_mnoethe_presentation.pdf

PLOTS = build/camera_image_0.pdf \
	build/camera_image_1.pdf \
	build/calibrated.pdf \
	build/raw_data.pdf \
	build/spectrum.pdf \
	build/hillas_disp_1.pdf \
	build/leakage.pdf \
	build/roc.pdf \
	build/skymap.pdf \
	build/tevcat.pdf \


build/phd_mnoethe_presentation.pdf: FORCE $(PLOTS) build/videos/gamma_twice_no_helium.mp4
	TEXINPUTS=tudobeamertheme:.:../thesis: \
	latexmk \
		--lualatex \
		--interaction=nonstopmode \
		--halt-on-error \
		--output-directory=build \
		--file-line-error \
		--shell-escape \
		phd_mnoethe_presentation.tex


preview: FORCE $(PLOTS) build/videos/gamma_twice_no_helium.mp4
	TEXINPUTS=tudobeamertheme:.:../thesis: \
	latexmk \
		--lualatex \
		--interaction=nonstopmode \
		--halt-on-error \
		--output-directory=build \
		--file-line-error \
		--shell-escape \
		-pvc \
		phd_mnoethe_presentation.tex


build/spectrum.pdf: ../thesis/build/spectrum_apa85.json ../configs/magic_jheap2015.yaml | build
	sed -e 's/"label": ".*",$$/"label": "Diese Arbeit",/' $< > /tmp/spectrum.json
	MATPLOTLIBRC=matplotlibrc_pgf TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	fact_plot_spectrum  \
		/tmp/spectrum.json \
		-p ../configs/magic_jheap2015_noref.yaml \
		-o $@

build/hillas_skewness.pdf: plots/plot_hillas_skewness.py | build
	MATPLOTLIBRC=matplotlibrc_pgf TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	python $< \
		-o $@

build/hillas_disp_1.pdf: plots/plot_hillas.py | build
	MATPLOTLIBRC=matplotlibrc_pgf TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	python $<


build/leakage.pdf: plots/plot_leakage.py | build
	MATPLOTLIBRC=matplotlibrc_pgf TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	python $<


build/tevcat.pdf: plots/plot_tevcat.py | build
	MATPLOTLIBRC=matplotlibrc_pgf TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	python $< $@


build/roc.pdf: plots/plot_roc.py ../build/apa85/cv_separator.hdf5 | build
	MATPLOTLIBRC=matplotlibrc_pgf TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	python $^ $@


build/skymap.pdf build/skymap_positions.pdf: plots/skymap_offregions.py | build
	MATPLOTLIBRC=matplotlibrc_pgf TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	python $< \
		../build/apa85/crab_dl3.hdf5 \
		`cat ../thesis/build/threshold_apa85.txt` \
		`cat ../thesis/build/theta2_cut_apa85.txt`


build/videos/%:  videos/%
	mkdir -p build/videos
	cp $< $@

build/camera_image_0.pdf build/camera_image_1.pdf build/calibrated.pdf build/raw_data.pdf: matplotlibrc_pgf plots/plot_reco.py | build
	MATPLOTLIBRC=matplotlibrc_pgf TEXINPUTS=$$(pwd): python plots/plot_reco.py


build:
	mkdir -p $@


FORCE:

clean:
	rm -rf build

.PHONY: all clean FORCE plots preview
