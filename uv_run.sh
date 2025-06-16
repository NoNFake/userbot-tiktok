# uv run -m usrbot

hour=3600 # 1 hour
timer=$((hour*6))


while true;do
    timeout $timer uv run -m usrbot
    echo "Restarting"
    sleep 1
done
