n_spams=$1 
start=$2
end=$3
type=$4
echo "Num steps: ${n_spams}"
for ((i = 0; i <= $n_spams; i++));
do
    echo "Step: ${i}, type: ${type}" 
    echo "Limit: ${start} -> ${end}"
    python src/data/get_block.py --start $start \\
     --end $end \\
     --type $type \\
done