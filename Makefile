DIR := ${CURDIR}
DATADIR=$(DIR)/data
DL2_DIR=$(DATADIR)/dl2
OUTDIR=$(DIR)/build

all: thesis/build/phd_mnoethe.pdf

thesis/build/phd_mnoethe.pdf: $(OUTDIR)/apa85/crab_dl3.hdf5
thesis/build/phd_mnoethe.pdf: $(OUTDIR)/apa95/crab_dl3.hdf5
thesis/build/phd_mnoethe.pdf: $(OUTDIR)/apa100/crab_dl3.hdf5
thesis/build/phd_mnoethe.pdf: $(OUTDIR)/apa85/crab_old_disp_dl3.hdf5
thesis/build/phd_mnoethe.pdf: $(OUTDIR)/apa85-mmcs6500/crab_dl3.hdf5



$(OUTDIR)/%/crab_dl3.hdf5 $(OUTDIR)/%/gamma_test_dl3.hdf5 $(OUTDIR)/%/proton_test_dl3.hdf5 $(OUTDIR)/%/helium_dl3.hdf5: FORCE
	make -f analysis.mk \
		CUTS_CONFIG=$(DIR)/configs/quality_cuts.yaml \
		AICT_CONFIG=$(DIR)/configs/aict.yaml \
		GAMMA_TRAIN_FRACTION=0.25 \
		GAMMA_TEST_FRACTION=0.75 \
		PROTON_TRAIN_FRACTION=0.25 \
		PROTON_TEST_FRACTION=0.75 \
		CRAB_FILE=$(DL2_DIR)/observations/v1.1.2/crab1314_v1.1.2.hdf5 \
		GAMMA_FILE=$(DL2_DIR)/simulations/v1.1.2/$*/gammas_wobble_corsika76900.hdf5 \
		GAMMA_DIFFUSE_FILE=$(DL2_DIR)/simulations/v1.1.2/$*/gammas_diffuse_corsika76900.hdf5 \
		PROTON_FILE=$(DL2_DIR)/simulations/v1.1.2/$*/protons_corsika76900.hdf5 \
		HELIUM_FILE=$(DL2_DIR)/simulations/v1.1.2/$*/helium4_corsika76900.hdf5 \
		OUTDIR=$(OUTDIR)/$* \
		$(OUTDIR)/$*/crab_dl3.hdf5 $(OUTDIR)/$*/gamma_test_dl3.hdf5 \
		$(OUTDIR)/$*/proton_test_dl3.hdf5 $(OUTDIR)/$*/helium_dl3.hdf5

$(OUTDIR)/apa85-mmcs6500/crab_dl3.hdf5 $(OUTDIR)/apa85-mmcs6500/gamma_test_dl3.hdf5 $(OUTDIR)/apa85-mmcs6500/proton_test_dl3.hdf5: FORCE
	make -f analysis.mk \
		CUTS_CONFIG=$(DIR)/configs/quality_cuts.yaml \
		AICT_CONFIG=$(DIR)/configs/aict_mmcs6500.yaml \
		PROTON_FILE=$(DL2_DIR)/simulations/v1.1.2/apa85/protons_mmcs6500.hdf5 \
		GAMMA_TRAIN_FRACTION=0.25 \
		GAMMA_TEST_FRACTION=0.75 \
		PROTON_TRAIN_FRACTION=0.75 \
		PROTON_TEST_FRACTION=0.25 \
		CRAB_FILE=$(DL2_DIR)/observations/v1.1.2/crab1314_v1.1.2.hdf5 \
		GAMMA_FILE=$(DL2_DIR)/simulations/v1.1.2/apa85/gammas_wobble_mmcs6500.hdf5 \
		GAMMA_DIFFUSE_FILE=$(DL2_DIR)/simulations/v1.1.2/apa85/gammas_diffuse_mmcs6500.hdf5 \
		OUTDIR=$(OUTDIR)/apa85-mmcs6500 \
		$(OUTDIR)/apa85-mmcs6500/crab_dl3.hdf5 \
		$(OUTDIR)/apa85-mmcs6500/gamma_test_dl3.hdf5 \
		$(OUTDIR)/apa85-mmcs6500/proton_test_dl3.hdf5

$(OUTDIR)/%/crab_old_disp_dl3.hdf5: scripts/old_disp_dl3.py build/%/crab_dl3.hdf5 build/%/crab_precuts.hdf5
	python scripts/old_disp_dl3.py \
		$(OUTDIR)/$*/crab_precuts.hdf5 \
		$(OUTDIR)/$*/crab_dl3.hdf5 \
		$@


thesis/build/phd_mnoethe.pdf:
	make -C thesis

FORCE:

.phony: all FORCE
