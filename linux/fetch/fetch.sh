#!/bin/bash
dest_dir=`pwd`
data_dir=~/data/topcoder
cd ~/src/topcoder/fetch
./fetch.py $@ $data_dir $dest_dir
