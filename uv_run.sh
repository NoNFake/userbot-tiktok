# uv run -m usrbot

timer=3600 # 1 hour

while true;do
    timeout $timer uv run -m usrbot
    echo "Restarting"
    sleep 1
done
