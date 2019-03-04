SHELL=bash
OUTDIR=build
MATPLOTLIBRC=plots/matplotlibrc
DATADIR=../data

all: build/phd_mnoethe.pdf # build/pdfa_compliance.xml


plots: $(addprefix build/plots/, $(addsuffix .pdf, \
	fact_pixels \
	data_gamma_comp_apa85 \
	data_gamma_comp_apa95 \
	data_gamma_comp_apa100 \
	star_pedvar \
	image_proton \
	image_gamma \
	image_muon \
	fluka_urqmd_comparison \
	coord_precision \
	old_new_comparison \
	data_mc_comparison \
	data_mc_comparison_all \
	data_mc_comparison_size_gt_500 \
	impact \
	proton_footprint \
	gamma_footprint \
	iron_footprint \
	iron_footprint_rgb \
	roc_example \
	4fgl_fact_sources \
	fact_ontime_half \
	gains \
	drs_calib \
	hillas_features \
	significances_apa85 \
	significances_apa95 \
	significances_apa100 \
	compare_old_disp \
	compare_old_disp_only_correct \
	proton_helium_spectrum \
	size_vs_true_energy \
	theta2_apa85 \
	theta2_apa95 \
	theta2_apa100 \
	skymap_apa85 \
	skymap_apa95 \
	skymap_apa100 \
	effective_area_apa85 \
	effective_area_apa95 \
	effective_area_apa100 \
	effective_area_apa85_bg \
	effective_area_apa95_bg \
	effective_area_apa100_bg \
	bias_resolution_apa85 \
	bias_resolution_apa95 \
	bias_resolution_apa100 \
	bias_resolution_all_apa85 \
	energy_migration_apa85 \
	energy_migration_apa95 \
	energy_migration_apa100 \
	sensitivity_apa85 \
	sensitivity_apa95 \
	sensitivity_apa100 \
	disp_metrics_apa85 \
	disp_metrics_apa95 \
	disp_metrics_apa100 \
	roc_vs_energy_apa85 \
	separator_performance_apa85 \
	))

plots: build/plots/spectrum_comparison.pgf
plots: build/plots/crab_sed.pgf

build/phd_mnoethe.pdf: build/r2_apa85.tex build/integral_sensitivity_apa85.tex build/event_num_table.tex


build/phd_mnoethe.pdf: plots FORCE
	latexmk \
		--lualatex \
		--interaction=nonstopmode \
		--halt-on-error \
		--output-directory=build \
		phd_mnoethe.tex


preview: plots FORCE
	latexmk \
		--lualatex \
		--interaction=nonstopmode \
		--halt-on-error \
		--output-directory=build \
		-pvc \
		phd_mnoethe.tex

build/plots/4fgl_fact_sources.pdf: $(DATADIR)/4fgl.fits


$(DATADIR)/4fgl.fits:
	curl -L -o $@ https://fermi.gsfc.nasa.gov/ssc/data/access/lat/8yr_catalog/gll_psc_v20.fit


build/pdfa_compliance.xml: build/phd_mnoethe.pdf
	verapdf --flavour 3u $^ | tee $@ | grep -Poh 'isCompliant="true"'


build/integral_sensitivity_%.tex: ../build/%/crab_dl3.hdf5 scripts/calc_integral_sensitivity.py build/threshold_%.txt build/theta2_cut_%.txt
	python scripts/calc_integral_sensitivity.py \
		$< $@ `cat build/threshold_$*.txt` `cat build/theta2_cut_$*.txt`


build/plots/%.pdf: plots/plot_%.py plots/matplotlibrc plots/header.tex | build/plots
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=$(MATPLOTLIBRC) \
		python $< $@ 


build/plots/%_half.pdf: plots/plot_%.py plots/matplotlibrc_half plots/header.tex | build/plots
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=$(MATPLOTLIBRC)_half \
		python $< $@ 


build/plots/fluka_urqmd_duration.pdf: plots/plot_fluka_urqmd_duration.py plots/matplotlibrc_half plots/header.tex | build/plots
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc_half \
		python $< $@ 


build/plots/gamma_footprint.pdf: $(DATADIR)/shower_footprints/gamma_1TeV.eventio.zst plots/plot_light_on_ground.py | build/plots
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=$(MATPLOTLIBRC)_third \
	python plots/plot_light_on_ground.py $< -r 250 -m 99.9 -o $@


build/plots/proton_footprint.pdf: $(DATADIR)/shower_footprints/proton_1TeV.eventio.zst plots/plot_light_on_ground.py | build/plots
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=$(MATPLOTLIBRC)_third \
	python plots/plot_light_on_ground.py $< -r 500 -m 99.9 -o $@


build/plots/iron_footprint.pdf: $(DATADIR)/shower_footprints/iron_10TeV.eventio.zst plots/plot_light_on_ground.py | build/plots
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=$(MATPLOTLIBRC)_third \
	python plots/plot_light_on_ground.py $< -r 500 -m 99.9 -o $@
	
build/plots/iron_footprint_rgb.pdf: $(DATADIR)/shower_footprints/iron_10TeV.eventio.zst plots/plot_light_on_ground_rgb.py | build/plots
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=$(MATPLOTLIBRC) \
	python plots/plot_light_on_ground_rgb.py $< -r 500 -m 99.9 -o $@

build/plots/significances_%.pdf build/threshold_%.txt build/theta2_cut_%.txt build/best_significance_%.txt: ../build/%/crab_dl3.hdf5 plots/plot_significances.py plots/matplotlibrc | build/plots
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc \
	python plots/plot_significances.py \
		$< \
		build/plots/significances_$*.pdf \
		build/best_significance_$*.txt \
		build/theta2_cut_$*.txt \
		build/threshold_$*.txt


build/plots/energy_migration_%.pdf: ../build/%/gamma_test_dl3.hdf5 plots/matplotlibrc | build/plots build/threshold_%.txt
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc \
	fact_plot_energy_migration \
		$< \
		--threshold=`cat build/threshold_$*.txt` \
		--theta2-cut=`cat build/theta2_cut_$*.txt` \
		-o $@


build/plots/bias_resolution_%.pdf: ../build/%/gamma_test_dl3.hdf5 plots/matplotlibrc | build/plots build/threshold_%.txt
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc \
	fact_plot_bias_resolution \
		$< \
		--threshold=`cat build/threshold_$*.txt` \
		--theta2-cut=`cat build/theta2_cut_$*.txt` \
		--e-low=316.23 \
		--e-high=50118.7 \
		--n-bins=11 \
		-o $@


build/plots/bias_resolution_all_%.pdf: ../build/%/gamma_test_dl3.hdf5 plots/matplotlibrc | build/plots build/threshold_%.txt
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc \
	fact_plot_bias_resolution \
		$< \
		--e-low=316.23 \
		--e-high=50118.7 \
		--n-bins=11 \
		-o $@


build/plots/compare_old_disp.pdf: plots/plot_compare_old_disp.py plots/matplotlibrc
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc \
	python plots/plot_compare_old_disp.py \
		../build/apa95/gamma_test.hdf5 \
		../build/apa95/gamma_test_dl3.hdf5 \
		0.8 \
		$@


build/plots/compare_old_disp_only_correct.pdf: plots/plot_compare_old_disp.py plots/matplotlibrc
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc \
	python plots/plot_compare_old_disp.py \
		../build/apa95/gamma_test.hdf5 \
		../build/apa95/gamma_test_dl3.hdf5 \
		0.8 \
		$@ \
		--only-correct-sign


build/plots:
	mkdir -p build/plots


build/disp_%_r2.tex build/disp_%_accuracy.tex: ../build/%/train_disp.log
	python scripts/disp_performance.py $< build/disp_$*


build/plots/disp_metrics_%.pdf: ../build/%/gamma_test_dl3.hdf5 plots/matplotlibrc plots/plot_disp_metrics.py | build/plots
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc \
		python plots/plot_disp_metrics.py $< $@ --threshold=`cat build/threshold_$*.txt`
	


build/plots/theta2_%.pdf: ../build/%/crab_dl3.hdf5 build/threshold_%.txt build/theta2_cut_%.txt   plots/matplotlibrc | build/plots
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc \
		fact_plot_theta_squared $< -o $@ \
		--threshold=`cat build/threshold_$*.txt` \
		--theta2-cut=`cat build/theta2_cut_$*.txt`


build/plots/theta2_old_disp_%.pdf: ../build/%/crab_old_disp_dl3.hdf5 build/threshold_%.txt plots/matplotlibrc | build/plots
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc \
		fact_plot_theta_squared $< -o $@ \
		--threshold=`cat build/threshold_$*.txt` \
		--theta2-cut=`cat build/theta2_cut_$*.txt`


build/plots/skymap_%.pdf: ../build/%/crab_dl3.hdf5 build/threshold_%.txt build/theta2_cut_%.txt   plots/matplotlibrc | build/plots
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc \
		fact_plot_skymap $< -o $@ \
		--threshold=`cat build/threshold_$*.txt` \
		--source="83.63308333°" "22.0145°" \
		--source-name="Crab Nebula"


build/plots/effective_area_%.pdf: ../build/%/gamma_test_dl3.hdf5 ../data/corsika_headers/gamma_headers_corsika76900.hdf5 build/threshold_%.txt build/theta2_cut_%.txt  plots/matplotlibrc | build/plots
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc \
		fact_plot_effective_area \
		../data/corsika_headers/gamma_headers_corsika76900.hdf5 \
		$< -o $@ \
		--threshold=0 --theta2-cut=inf \
		--threshold=`cat build/threshold_$*.txt` --theta2-cut=inf \
		--threshold=`cat build/threshold_$*.txt` \
		--theta2-cut=`cat build/theta2_cut_$*.txt` \
		--e-low=316.23 \
		--e-high=50118.7 \
		--n-bins=11


build/plots/effective_area_%_bg.pdf: ../build/%/gamma_test_dl3.hdf5 ../build/%/proton_test_dl3.hdf5 ../data/corsika_headers/gamma_headers_corsika76900.hdf5 build/threshold_%.txt build/theta2_cut_%.txt  plots/plot_effective_area_bg.py plots/matplotlibrc | build/plots
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc \
		python plots/plot_effective_area_bg.py \
		../data/corsika_headers/gamma_headers_corsika76900.hdf5 \
		../build/$*/gamma_test_dl3.hdf5 \
		../data/corsika_headers/proton_headers_corsika76900.hdf5 \
		../build/$*/proton_test_dl3.hdf5 \
		-o $@ \
		--threshold=0 --theta2-cut=inf \
		--threshold=`cat build/threshold_$*.txt` \
		--theta2-cut=`cat build/theta2_cut_$*.txt` \
		--e-low=316.23 \
		--e-high=50118.7 \
		--n-bins=11



.PRECIOUS: build/sensitivity_obs_%.csv
build/sensitivity_obs_%.csv: ../build/%/crab_dl3.hdf5 scripts/calc_sensitivity_observations.py
build/sensitivity_obs_%.csv: build/threshold_%.txt build/theta2_cut_%.txt
	python scripts/calc_sensitivity_observations.py \
		../build/$*/crab_dl3.hdf5 \
		`cat build/threshold_$*.txt` \
		`cat build/theta2_cut_$*.txt` \
		$@



.PRECIOUS: build/sensitivity_sim_%.csv
build/sensitivity_sim_%.csv: ../build/%/gamma_test_dl3.hdf5 ../build/%/proton_test_dl3.hdf5
build/sensitivity_sim_%.csv: scripts/calc_sensitivity_observations.py
build/sensitivity_sim_%.csv: build/threshold_%.txt build/theta2_cut_%.txt
	python scripts/calc_sensitivity_simulations.py \
		../build/$*/gamma_test_dl3.hdf5 \
		../data/corsika_headers/gamma_headers_corsika76900.hdf5 \
		../build/$*/proton_test_dl3.hdf5 \
		../data/corsika_headers/proton_headers_corsika76900.hdf5  \
		`cat build/threshold_$*.txt` \
		`cat build/theta2_cut_$*.txt` \
		$@



build/plots/sensitivity_%.pdf: plots/plot_compare_sensitivity.py
build/plots/sensitivity_%.pdf: build/sensitivity_sim_%.csv build/sensitivity_obs_%.csv
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc \
	python plots/plot_compare_sensitivity.py $@ \
		--sensitivity Simulated build/sensitivity_sim_$*.csv \
		--sensitivity Observed build/sensitivity_obs_$*.csv \



build/spectrum_%.json: ../build/%/crab_dl3.hdf ../build/%/gamma_test_dl3.hdf5 
build/spectrum_%.json: ../configs/unfolding.yaml
	fact_unfold_observations \
		../configs/unfolding.yaml \
		../build/$*/crab_dl3.hdf5 \
		../build/$*/gamma_test_dl3.hdf5 \
		../data/corsika_headers/gamma_headers_corsika76900.hdf5 \
		--label="$$\param{APA} = \SI{`echo $* | tr -d "[:alpha:]"`}{\percent}$$" \
		--threshold=`cat build/threshold_$*.txt` \
		--theta2_cut=`cat build/theta2_cut_$*.txt` \
		$@


build/plots/spectrum_comparison.pgf: build/spectrum_apa85.json build/spectrum_apa95.json build/spectrum_apa100.json ../configs/magic_jheap2015.yaml
	MATPLOTLIBRC=plots/matplotlibrc TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	fact_plot_spectrum build/spectrum_apa{85,95,100}.json \
		-p ../configs/magic_jheap2015.yaml \
		-o $@

build/plots/crab_sed.pgf: ../data/crab_mwl.fits.gz plots/plot_crab_sed.py
	MATPLOTLIBRC=plots/matplotlibrc TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	python plots/plot_crab_sed.py $@

build/r2_%.tex: scripts/calc_r2_score.py ../build/%/cv_regressor.hdf5 | build
	python scripts/calc_r2_score.py ../build/$*/cv_regressor.hdf5 $@


build/plots/roc_vs_energy_%.pdf: plots/plot_roc_vs_energy.py plots/matplotlibrc
build/plots/roc_vs_energy_%.pdf: ../build/%/gamma_test_dl3.hdf5 ../build/%/proton_test_dl3.hdf5
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc \
	python plots/plot_roc_vs_energy.py \
		../build/$*/gamma_test_dl3.hdf5 \
		../build/$*/proton_test_dl3.hdf5 \
		$@



build/plots/image_proton.pdf: plots/plot_image.py plots/matplotlibrc plots/header.tex
	MATPLOTLIBRC=plots/matplotlibrc TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	python plots/plot_image.py \
		../data/ceres_proton_diffuse_6d_run_00010000_az270-280_zd07-08_dl1.fits.gz \
		15 \
		$@


build/plots/image_gamma.pdf: plots/plot_image.py plots/matplotlibrc plots/header.tex
	MATPLOTLIBRC=plots/matplotlibrc TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	python plots/plot_image.py \
		../data/ceres_gamma_wobble_0.6d_run_00030241_az000-010_zd00-01_dl1.fits.gz \
		5 \
		$@


build/plots/image_muon.pdf: plots/plot_image.py plots/matplotlibrc plots/header.tex
	MATPLOTLIBRC=plots/matplotlibrc TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	python plots/plot_image.py \
		../data/ceres_mu_minus_diffuse_6d_run_00000001_az000-000_zd00-00_dl1.fits.gz \
		4 \
		$@

build/plots/fluka_urqmd_comparison.pdf: $(DATADIR)/dl2/simulations/v1.1.2/fluka_urqmd/protons_fluka_corsika76900.hdf5
build/plots/fluka_urqmd_comparison.pdf: $(DATADIR)/dl2/simulations/v1.1.2/fluka_urqmd/protons_urqmd_corsika76900.hdf5
build/plots/fluka_urqmd_comparison.pdf: configs/proton_urqdm_fluka_comparison.yaml
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc_small \
	fact_plot_data_mc_compare \
	$< $@

build/plots/old_new_comparison.pdf: configs/mc_comp_old_new.yaml
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc_small \
	fact_plot_data_mc_compare \
	$< $@


build/plots/data_mc_comparison.pdf: configs/data_mc_comp.yaml
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc_data_mc \
	fact_plot_data_mc_compare \
	$< $@


build/plots/data_mc_comparison_all.pdf: configs/data_mc_comp_all.yaml
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc_data_mc \
	fact_plot_data_mc_compare \
	$< $@


build/plots/data_mc_comparison_size_gt_500.pdf: configs/data_mc_comp_size_gt_500.yaml
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=plots/matplotlibrc_data_mc \
	fact_plot_data_mc_compare \
	$< $@

build/plots/data_gamma_comp_apa%.pdf: plots/plot_data_gamma_comp.py plots/matplotlibrc plots/header.tex | build/plots
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=$(MATPLOTLIBRC) \
		python $< $* $@ 


build/test_spectrum.json: ../build/apa85/gamma_test_dl3.hdf5
build/test_spectrum.json: ../configs/unfolding.yaml | $(OUTDIR)
	fact_unfold_simulations \
		../configs/unfolding.yaml \
		../build/apa85/gamma_test_dl3.hdf5 \
		../data/corsika_headers/gamma_headers_corsika76900.hdf5 \
		$@ \
		--obstime='91 h'


build/plots/test_spectrum.pdf: build/test_spectrum.json
build/plots/test_spectrum.pdf: configs/production_spectrum.yaml
build/plots/test_spectrum.pdf: plots/matplotlibrc plots/header.tex | $(OUTDIR)/plots
	MATPLOTLIBRC=plots/matplotlibrc \
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	fact_plot_spectrum \
		build/test_spectrum.json \
		-p configs/production_spectrum.yaml \
		-o $@


build/plots/separator_performance_apa%.pdf: plots/matplotlibrc plots/header.tex | build/plots
	TEXINPUTS=$$(pwd)/plots:$$(pwd): \
	MATPLOTLIBRC=$(MATPLOTLIBRC) \
		aict_plot_separator_performance ../configs/aict.yaml \
		../build/apa$*/cv_separator.hdf5 \
		../build/apa$*/separator.pkl \
		-o $@ 

build/event_num_table.tex:
	python scripts/event_num_table.py


FORCE:

clean:
	rm -rf build


.PHONY: all clean FORCE plots
