from pathlib import Path
import logging
log = logging.getLogger(__name__)

FILES_PATH = Path(__file__).parent

message: str = ''
for files in FILES_PATH.iterdir():
    if files.is_dir():
        continue
    
    with open(files, 'r') as f:
        lines = f.read().split('\n')
        lines: list = lines[0:2]

        # if list size is less than 2 skip
        if len(lines) < 2:
            continue

        command = lines[0].split('=')
        info = lines[1].split('=')

        if len(command) < 2:
            continue
        
        inf_message = f"\n{command[1]}: {info[1]}"
        # print( f"{command[1]}: {info[1]}")
        inf_message = inf_message.replace('"', '')
        # inf_message = inf_message.replace(' .', '.')
        

        message += inf_message 
print(message)
        