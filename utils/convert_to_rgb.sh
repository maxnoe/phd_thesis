#!/bin/bash


# convert a pdf file to sRGB for inclusion in PDF/A

if [[ "$1" == "--help" || "$1" == "-h" || -z "$1" || -z "$2" ]]; then
	echo "Convert a pdf file to RGB color space"
	echo
	echo "Usage: convert_ro_rgb <inputfile> <outputfile>"
fi

if [[ -z "$1" || -z "$2" ]]; then
	exit 1
fi

gs \
	-sDEVICE=pdfwrite \
	-dBATCH \
	-dNOPAUSE \
	-dCompatibilityLevel=1.7 \
	-dColorConversionStrategy="/sRGB" \
	-dProcessColorModel="/DeviceRGB" \
	-dColorConversionStrategyForImages=/DeviceRGB \
	-o $2 \
	$1
