#!/bin/bash

if [ -n $1 ]; then
    src=$1
else
    src="log_archive/"
fi

dest="processed_data/"

if [ ! -e $dest ]; then
    mkdir $dest
fi

echo "Writing to: $dest"

function load_data {
    fullname=$dest$3".txt"
    echo "" > $fullname
    cat $src$1 | grep $2 | cut -d":" -f2 > $fullname
}

for file in `ls $src`
do
    echo "Processing: $file"
    load_data $file "Average_fitness" $file"_avg"
    load_data $file "Max_fitness" $file"_max"
    load_data $file "Min_fitness" $file"_min"
done
