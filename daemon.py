import json
from time import sleep
import datetime
import logging
import subprocess
import os
from rich import print
from rich.console import Console
from rich.logging import RichHandler


def crash(code):
    input("Press enter to exit")
    exit(code)

logging.basicConfig(
    level="INFO",
    format="%(message)s", datefmt="[%X]", 
    handlers=[RichHandler()]
)

console = Console()

# Load plugins
command_executors = {}
files = os.listdir("./plugins")
for file in files:
    if file.endswith(".py"):
        try:
            exec(f"import plugins.{file[:-3]} as {file[:-3]}")
            this = {
                'name': file[:-3],
                'author': eval(f"{file[:-3]}.plugin['author']"),
                'version': eval(f"{file[:-3]}.plugin['version']"),
                'export': eval(f"{file[:-3]}.plugin['export']")
            }
            logging.info(f"Loaded plugin [purple]{file}[/] ({this['version']}) by [purple]{this['author']}[/]", extra={"markup": True})
            for cmd in this['export']:
                command_executors[cmd] = this['name']
        except Exception as e:
            console.print_exception()
            logging.error(f"Error while loading plugin {file}. See above.")
    
with open('plugins.json', 'w') as f:
    json.dump({'command_executors': command_executors}, f, indent=4)

try:
    with open('tasks.json') as f:
        tasks = json.load(f)['tasks']
except FileNotFoundError:
    with open('tasks.json', 'w') as f:
        f.write('{"tasks": []}')
    logging.warning("Default tasks.json file created")
    tasks = []
except json.JSONDecodeError:
    logging.critical("JSON file is corrupted")
    crash(-1)
except KeyError:
    logging.critical("Wrong format in JSON file")
    crash(-1)

logging.info("Daemon started")
logging.info(f"Loaded {len(tasks)} tasks")
logging.info(f"Loaded {len(command_executors)} executors")

while True:
    while datetime.datetime.now().second != 0:
        try:
            sleep(1)
        except KeyboardInterrupt:
            logging.warning("KeyboardInterrupt received, shutting down daemon...")
            exit(0)
    try:
        with open('tasks.json') as f:
            ntasks = json.load(f)['tasks']
        logging.debug(f"Read tasks.json file successfully")
    except FileNotFoundError:
        logging.warning("Could not refresh tasks as tasks.json file is missing. Rerun the daemon to create it.")
    except json.JSONDecodeError:
        logging.warning("Could not refresh tasks as tasks.json file is corrupted")
    except KeyError:
        logging.warning("Could not refresh tasks as tasks.json file is in wrong format")
    finally:
        if ntasks != tasks:
            logging.warning(f"Detect task changes, reloading.")
            logging.info(f"Loaded {len(ntasks)} tasks")
            tasks = ntasks
    nowtime = datetime.datetime.now().strftime("%H:%M")
    logging.debug(f"Current time: {nowtime}")
    for task in tasks:
        if task['time'] == nowtime:
            logging.info(f"Executing task id {task['id']}")
            if task['type'] == "command":
                try:
                    subprocess.run(task['command'], shell=True)
                except Exception as e:
                    console.print_exception()
                    logging.error(f"Error while executing task. see above.")
            elif task['type'] == "plugin":
                try:
                    executor = task['command'].split(':')[0]
                    plug = command_executors[executor]
                    args = ' '.join(task['command'].split(':')[1:])
                    ret = eval(f"{plug}.{executor}({args})")
                    logging.info(f"Executor finished with return {ret}.")
                except Exception as e:
                    console.print_exception()
                    logging.error(f"Error while executing task. see above.")
    try:
        sleep(1)
    except KeyboardInterrupt:
        logging.warning("KeyboardInterrupt received, shutting down daemon...")
        exit(0)