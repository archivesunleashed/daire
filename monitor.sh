fswatch --batch-marker=EOF -xn . | while read file event; do 
    if [ $file = "EOF" ]; then
        for file in "${list[@]}";do
            relative=${file#/Users/johnson/aut}
            echo -e "\033[1;31m${relative}\033[0m"
            exp-tuna 'Tp14X!4m' scp -r $file x65han@tuna.cs.uwaterloo.ca:/home/x65han/aut/${relative}
        done
        echo -e "\033[1;32m --- BATCH --- \033[0m\n"
        list=()
        say done
    else
        list+=($file)
    fi
done
