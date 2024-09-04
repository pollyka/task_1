#!/bin/bash


clear
echo 'Введите назввание '
read FileName
FileName=$(find . -maxdepth 1 -type f -name "$FileName*" -printf '%f\n')

var=1
echo 'Банк для выбора файлов для чтения: n_05 n_1 n_2 n_10 n_30 n_50 n_75 n_100 n_120 n_140 n_160 n_180 n_200'
echo 'Банк для выбора pileup: p_05 p_1 p_2 p_10 p_30 p_50 p_75 p_100 p_120 p_140 p_160 p_180 p_200'
echo 'Введите имена входных файлов для чтения, без запятых (Например: n_05 n_1) '
read f
f="-f${f}"
echo 'Введите pileup, (Hапример: p_05 p_1 p_2)'
read p
p="-p${p}"

echo 'Выберите ограничение на данные'
read t
t="-t${t}"


while [ $var -ne 2 ]
do
    echo $var
    if [ $var -eq 1 ]
    then
        python3 "$FileName" "$f" "$p" "$t"
#    else
#        python3 task_2.py "$f" "$p"
    fi
    var=$((var+1))
done



# elif [ $var -eq 2 ]
# then
#     hadd -f output.root HFOC_1.0.root HFOC2_2.root 
#     python3 task_2.py "$f"
# else
#     f="output.root"
#     f="-f${f}"
#     python3 plot.py "$f"



















