for ((i = 0; i <= 10; i++));
do
    echo "Try ${i}" time
    python src/data/get_block.py
done