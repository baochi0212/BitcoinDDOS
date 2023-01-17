n_spams=$1 
echo "Num steps: ${n_spams}"
for ((i = 0; i <= $n_spams; i++));
do
    echo "Step: ${i}" 
    python src/data/get_block.py
done