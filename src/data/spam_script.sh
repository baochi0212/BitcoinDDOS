n_spams=$1 
for ((i = 0; i <= $n_spams; i++));
do
    echo "Try ${i}" time
    python src/data/get_block.py
done