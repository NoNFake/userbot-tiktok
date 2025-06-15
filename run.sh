# timer=10

# python -m usrbot
timer=10 #10minutes

while true;do
    timeout $timer python -m usrbot
    echo "Restarting"
    sleep 1
done
