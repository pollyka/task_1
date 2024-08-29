#!/bin/bash


# clear
var=1

while [ $var -ne 4 ]
do
    echo $var
    if [ $var -eq 1 ]
    then
        echo 'Запуск первого файла: Введите назввание task_1'
        read FileName
        FileName=$(find . -maxdepth 1 -type f -name "$FileName*" -printf '%f\n')

        echo 'Банк для выбора файлов для чтения: n_05 n_1 n_2 n_10 n_30 n_50 n_75 n_100 n_120 n_140 n_160 n_180 n_200'
        echo 'Банк для выбора pileup: p_05 p_1 p_2 p_10 p_30 p_50 p_75 p_100 p_120 p_140 p_160 p_180 p_200'
        echo 'Введите имена файлов для чтения, без запятых (Например: n_05 n_1) '
        read f
        f="-f${f}"
        echo 'Введите puleup, (Hапример: p_05 p_1 p_2)'
        read p
        p="-p${p}"
        python3 "$FileName" "$f" "$p"
        var=2
    elif [ $var -eq 2 ]
    then
        echo 'Запуск второго файла: Введите назввание task_2'
        read FileName
        FileName=$(find . -maxdepth 1 -type f -name "$FileName*" -printf '%f\n')
        echo 'Банк для выбора файлов для чтения: o_05 o_1 o_2 o_10 o_30 o_50 o_75 o_100 o_120 o_140 o_160 o_180 o_200'
        echo 'Банк для выбора pileup: p_05 p_1 p_2 p_10 p_30 p_50 p_75 p_100 p_120 p_140 p_160 p_180 p_200'
        echo 'Введите имена файлов для чтения, без запятых (Например: o_05 o_1) '
        read f

        f="-f${f}"

        echo 'Введите puleup, (Hапример: p_05)'
        read p

        p="-p${p}"
        python3 "$FileName" "$f" "$p"
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




















