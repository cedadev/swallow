#!/bin/bash
#
#  This script will:
#   - optionally install miniconda (set initall_minconda=1)
#   - install a conda environment containing everything needed for swallow
#   - create a setup script and an exported yml file from that environment

set -ex

mc_path=/usr/local/Miniconda3-py39_4.9.2-Linux-x86_64
mc_env=swallow
initial_yml_file=${mc_env}_initial.yml
full_yml_file=${mc_env}_full.yml
setup_file=./setup-$mc_env.sh
install_miniconda=0

if [ $install_miniconda -eq 1 ]
then
    installer_url=https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    installer_filename=$(basename $installer_url)
    rm -fr $installer_filename $mc_path
    wget $installer_url
    bash $installer_filename -b -p $mc_path
else
    if [ ! -e $mc_path/bin/conda ]
    then
	echo "$mc_path does not seem to contain an existing conda installation"
	exit 1
    fi
    rm -fr $mc_path/envs/$mc_env
fi

rm -fr $initial_yml_file $full_yml_file $setup_file

cat >> $setup_file <<EOF
if [ -z "\$CONDA_PREFIX" ]
then
    . $mc_path/bin/activate
else
    echo "Miniconda already set up"
fi
EOF

cat > $initial_yml_file <<EOF
name: $mc_env
channels:
  - conda-forge
  - defaults
dependencies:
  - pywps>=4.4.5
  - jinja2
  - click
  - psutil
  - numpy
  - pandas
  - scitools-iris
  - matplotlib
  - cartopy
  - pyproj
EOF

. $setup_file
conda install -y -c conda-forge mamba
mamba env create -n $mc_env -f $initial_yml_file
conda deactivate

echo "conda activate $mc_env" >> $setup_file
. $setup_file
conda env export > $full_yml_file
conda deactivate
