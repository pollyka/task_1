#!/bin/bash


# clear
var=1
echo 'Банк для выбора файлов для чтения: n_05 n_1 n_2 n_10 n_30 n_50 n_75 n_100 n_120 n_140 n_160 n_180 n_200'
echo 'Банк для выбора pileup: p_05 p_1 p_2 p_10 p_30 p_50 p_75 p_100 p_120 p_140 p_160 p_180 p_200'
echo 'Введите имена входных файлов для чтения, без запятых (Например: n_05 n_1) '
read f
f="-f${f}"
echo 'Введите pileup, (Hапример: p_05 p_1 p_2)'
read p
p="-p${p}"

while [ $var -ne 4 ]
do
    echo $var
    if [ $var -eq 1 ]
    then
        python3 task_1.py "$f" "$p"
        var=2
    elif [ $var -eq 2 ]
    then

        python3 task_2.py "$f" "$p"
        var=3

    else

        hadd -f output.root HFOC1_1.root HFOC2_2.root HFOC10_10.root HFOC30_30.root HFOC50_50.root HFOC75_75.root HFOC100_100.root
        #  HFOC05_05.root HFOC75_75.root HFOC100_100.root HFOC120_120.root HFOC140_140.root HFOC160_160.root HFOC180_180.root HFOC200_200.root
        f="o_1"
        f="-f${f}"
        python3 plot.py "$f"
        var=4
    fi
done




















