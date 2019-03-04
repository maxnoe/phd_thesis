$(OUTDIR)/crab_precuts.hdf5: $(CRAB_FILE)  $(CUTS_CONFIG) | $(OUTDIR)
	aict_apply_cuts $(CUTS_CONFIG) $< $@ --chunksize=100000

$(OUTDIR)/crab1415_precuts.hdf5: $(CRAB1415_FILE)  $(CUTS_CONFIG) | $(OUTDIR)
	aict_apply_cuts $(CUTS_CONFIG) $< $@ --chunksize=100000

$(OUTDIR)/proton_precuts.hdf5: $(PROTON_FILE)  $(CUTS_CONFIG) | $(OUTDIR)
	aict_apply_cuts $(CUTS_CONFIG) $< $@ --chunksize=100000


$(OUTDIR)/helium_precuts.hdf5: $(HELIUM_FILE)  $(CUTS_CONFIG) | $(OUTDIR)
	aict_apply_cuts $(CUTS_CONFIG) $< $@ --chunksize=100000

$(OUTDIR)/gamma_precuts.hdf5: $(GAMMA_FILE)  $(CUTS_CONFIG) | $(OUTDIR)
	aict_apply_cuts $(CUTS_CONFIG) $< $@ --chunksize=100000

$(OUTDIR)/gamma_diffuse_precuts.hdf5: $(GAMMA_DIFFUSE_FILE)  $(CUTS_CONFIG) | $(OUTDIR)
	aict_apply_cuts $(CUTS_CONFIG) $< $@ --chunksize=100000


# Split gamma data into
# * a training set and a test set for irf / unfolding
$(OUTDIR)/gamma_train.hdf5 $(OUTDIR)/gamma_test.hdf5: $(OUTDIR)/gamma_precuts.hdf5
	aict_split_data $(OUTDIR)/gamma_precuts.hdf5 $(OUTDIR)/gamma \
		-f $(GAMMA_TRAIN_FRACTION) -n train \
		-f $(GAMMA_TEST_FRACTION) -n test \
		--chunksize=100000
		

# Split proton data into a training set for the separation and a test set
$(OUTDIR)/proton_train.hdf5 $(OUTDIR)/proton_test.hdf5: $(OUTDIR)/proton_precuts.hdf5
	aict_split_data $(OUTDIR)/proton_precuts.hdf5 $(OUTDIR)/proton \
		-f $(PROTON_TRAIN_FRACTION) -n train \
		-f $(PROTON_TEST_FRACTION) -n test \
		--chunksize=1000000


$(OUTDIR)/separator.pkl $(OUTDIR)/cv_separator.hdf5: $(AICT_CONFIG) $(OUTDIR)/proton_train.hdf5 $(OUTDIR)/gamma_diffuse_precuts.hdf5 
	aict_train_separation_model $(AICT_CONFIG) \
		$(OUTDIR)/gamma_diffuse_precuts.hdf5 \
		$(OUTDIR)/proton_train.hdf5 \
		$(OUTDIR)/cv_separator.hdf5 \
		$(OUTDIR)/separator.pkl \
		2>&1 | tee $(OUTDIR)/train_separator.log
		

$(OUTDIR)/energy.pkl $(OUTDIR)/cv_regressor.hdf5: $(AICT_CONFIG) $(OUTDIR)/gamma_diffuse_precuts.hdf5
	aict_train_energy_regressor $(AICT_CONFIG) \
		$(OUTDIR)/gamma_diffuse_precuts.hdf5 \
		$(OUTDIR)/cv_regressor.hdf5 \
		$(OUTDIR)/energy.pkl \
		2>&1 | tee $(OUTDIR)/train_regressor.log
		

$(OUTDIR)/disp.pkl $(OUTDIR)/sign.pkl $(OUTDIR)/cv_disp.hdf5: $(AICT_CONFIG) $(OUTDIR)/gamma_diffuse_precuts.hdf5
	aict_train_disp_regressor $(AICT_CONFIG) \
		$(OUTDIR)/gamma_diffuse_precuts.hdf5 \
		$(OUTDIR)/cv_disp.hdf5 \
		$(OUTDIR)/disp.pkl \
		$(OUTDIR)/sign.pkl \
		2>&1 | tee $(OUTDIR)/train_disp.log


$(OUTDIR)/crab_dl3.hdf5: $(addprefix $(OUTDIR)/, crab_precuts.hdf5 separator.pkl energy.pkl disp.pkl sign.pkl)
	fact_to_dl3 $(AICT_CONFIG) \
		$< \
		$(OUTDIR)/separator.pkl \
		$(OUTDIR)/energy.pkl \
		$(OUTDIR)/disp.pkl \
		$(OUTDIR)/sign.pkl \
		$@ \
		--chunksize=100000 --yes


$(OUTDIR)/crab1415_dl3.hdf5: $(addprefix $(OUTDIR)/, crab1415_precuts.hdf5 separator.pkl energy.pkl disp.pkl sign.pkl)
	fact_to_dl3 $(AICT_CONFIG) \
		$< \
		$(OUTDIR)/separator.pkl \
		$(OUTDIR)/energy.pkl \
		$(OUTDIR)/disp.pkl \
		$(OUTDIR)/sign.pkl \
		$@ \
		--chunksize=100000 --yes

$(OUTDIR)/proton_%_dl3.hdf5: $(addprefix $(OUTDIR)/, proton_%.hdf5 separator.pkl energy.pkl disp.pkl sign.pkl)
	fact_to_dl3 $(AICT_CONFIG) \
		$< \
		$(OUTDIR)/separator.pkl \
		$(OUTDIR)/energy.pkl \
		$(OUTDIR)/disp.pkl \
		$(OUTDIR)/sign.pkl \
		--random-source \
		--wobble-distance=0.6 \
		$@ \
		--chunksize=100000 --yes


$(OUTDIR)/helium_dl3.hdf5: $(addprefix $(OUTDIR)/, helium_precuts.hdf5 separator.pkl energy.pkl disp.pkl sign.pkl)
	fact_to_dl3 $(AICT_CONFIG) \
		$< \
		$(OUTDIR)/separator.pkl \
		$(OUTDIR)/energy.pkl \
		$(OUTDIR)/disp.pkl \
		$(OUTDIR)/sign.pkl \
		--random-source \
		--wobble-distance=0.6 \
		$@ \
		--chunksize=100000 --yes

$(OUTDIR)/%_dl3.hdf5: $(addprefix $(OUTDIR)/, %.hdf5 separator.pkl energy.pkl disp.pkl sign.pkl)
	fact_to_dl3 $(AICT_CONFIG) \
		$< \
		$(OUTDIR)/separator.pkl \
		$(OUTDIR)/energy.pkl \
		$(OUTDIR)/disp.pkl \
		$(OUTDIR)/sign.pkl \
		$@ \
		--chunksize=100000 --yes

$(OUTDIR)/separator_performance.pdf: $(AICT_CONFIG) $(OUTDIR)/separator.pkl $(OUTDIR)/cv_separator.hdf5 | $(OUTDIR)
	aict_plot_separator_performance  $(AICT_CONFIG) \
		$(OUTDIR)/cv_separator.hdf5 \
		$(OUTDIR)/separator.pkl \
		-o $(OUTDIR)/separator_performance.pdf

$(OUTDIR)/regressor_performance.pdf: $(AICT_CONFIG) $(OUTDIR)/energy.pkl $(OUTDIR)/cv_regressor.hdf5 | $(OUTDIR)
	aict_plot_regressor_performance  $(AICT_CONFIG) \
		$(OUTDIR)/cv_regressor.hdf5 \
		$(OUTDIR)/energy.pkl \
		-o $(OUTDIR)/regressor_performance.pdf


$(OUTDIR)/theta2_plot.pdf: $(OUTDIR)/crab_dl3.hdf5
	fact_plot_theta_squared \
		$< \
		--threshold=$(PREDICTION_THRESHOLD_SOURCE) \
		--theta2-cut=$(THETA2_CUT_SOURCE) \
		--preliminary \
		-o $@ \
		2>&1 | tee $(OUTDIR)/significance.txt

$(OUTDIR)/theta2_plot_1415.pdf: $(OUTDIR)/crab1415_dl3.hdf5
	fact_plot_theta_squared \
		$< \
		--threshold=$(PREDICTION_THRESHOLD_SOURCE) \
		--theta2-cut=$(THETA2_CUT_SOURCE) \
		--preliminary \
		-o $@ \
		2>&1 | tee $(OUTDIR)/significance1415.txt


$(OUTDIR): 
	mkdir -p $(OUTDIR)

clean:
	rm -rf $(OUTDIR)

.PHONY: all clean

