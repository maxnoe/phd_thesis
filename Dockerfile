from ubuntu:18.04 AS build


# update and install git, curl, make
RUN apt update \
	&& apt upgrade --yes \
	&& apt install --yes --no-install-recommends \
		git \
		make \
		ca-certificates \
		gpg \
		wget \
	&& rm -rf /var/lib/apt/lists/*


# install miniconda
ARG MINICONDA="Miniconda3-4.7.12-Linux-x86_64.sh"
RUN echo $MINICONDA \
	&& wget -q "https://repo.anaconda.com/miniconda/$MINICONDA" \
  	&& bash $MINICONDA -b -p /opt/conda \
  	&& ln -sf /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh \
  	&& rm -rf $MINICONDA

ADD full_environment.yaml /opt/
RUN /opt/conda/bin/conda env create -n phd_mnoethe -f /opt/full_environment.yaml \
	&& /opt/conda/bin/conda clean -afqy \
	&& find /opt/conda -follow -type f -name '*.pyc' -delete \
	&& rm -rf /root/.cache/pip

# Install TeXLive
RUN /opt/conda/envs/phd_mnoethe/bin/install_texlive -v -t 2019 -p /opt/texlive \
	--collections="-aDupG" -i "koma-script,latexmk,pdfx,ms,xcolor,pdfescape,letltxmacro,bitset,xmpincl,xpatch,l3packages,fontspec,microtype,fontawesome5,csquotes,mathtools,pdflscape,unicode-math,siunitx,enumitem,wrapfig,booktabs,genmisc,float,ncctools,caption,biblatex,glossaries,pgf,tikz-feynman,tikz-3dplot,todonotes,pgfopts,mfirstuc,textcase,xfor,datatool,tracklang,libertinus-fonts,fira,xits,biber,placeins,listings,babel-german,babel-english,glossaries-german,glossaries-english,xindy,type1cm"

ENV PATH "/opt/texlive/2019/bin/x86_64-linux:$PATH"
ENTRYPOINT ["bash", "-l"]
