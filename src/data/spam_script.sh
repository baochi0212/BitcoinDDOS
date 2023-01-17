n_spams=$1 
start=$2
type=$3
end=$4
echo "Num steps: ${n_spams}"
for ((i = 0; i <= $n_spams; i++));
do
    echo "Step: ${i}" 
    python src/data/get_block.py --start $start \
     --end $end \
     --type $type \
done