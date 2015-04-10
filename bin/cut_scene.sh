#!/bin/bash
#echo "Test bash"
echo "$baslama"
echo "$sure"
echo "$word"
echo "$count"
array=($baslama)
FILM_DIR="../filmler"
MOVIE=$1
INP="$FILM_DIR/$MOVIE/$MOVIE.mp4"
START=$2
LENGTH=$3
SID=$4
OUT="$FILM_DIR/$MOVIE/scenes/$SID.mp4"
echo $INP $OUT

ffmpeg -i $INP -ss $START -t $LENGTH -async 1 -strict -2 $OUT
# for var in ${array[*]}
# do
# ffmpeg -i /home/jaseen/Desktop/tezz/The.Avengers.mp4 -ss $var -t 00:00:10 -async 1 -strict -2 /home/jaseen/Desktop/tezz/$word/$count.mp4
# done
# date
