import json
from time import sleep
import datetime
import logging
import subprocess
import os
from rich import print
from rich.console import Console
from rich.logging import RichHandler

# Pause on crash
def crash(code):
    input("Press enter to exit")
    exit(code)

# Logging setup
logging.basicConfig(
    level="INFO",
    format="%(message)s", datefmt="[%X]", 
    handlers=[RichHandler()]
)

console = Console()

def load_tasks(create_on_missing=False):
    try:
        # Load tasks
        with open('tasks.json') as f:
            return json.load(f)['tasks']
    except FileNotFoundError:
        if create_on_missing:
            # Create default tasks.json file
            with open('tasks.json', 'w') as f:
                f.write('{"tasks": []}')
            logging.warning("Default tasks.json file created")
            return []
        else:
            return None
    except json.JSONDecodeError:
        # If the file is corrupted, crash
        return -1
    except KeyError:
        # If the file is in wrong format
        return -2

def load_plugins(previous={}):
    command_executors = previous
    files = os.listdir("./plugins") # List all files in plugins directory
    for file in files:
        if file.endswith(".py") and file[:-3] not in previous.values():
            try:
                exec(f"import plugins.{file[:-3]} as {file[:-3]}") # Import the plugin
                this = {
                    'name': file[:-3],
                    'author': eval(f"{file[:-3]}.plugin['author']"),
                    'version': eval(f"{file[:-3]}.plugin['version']"),
                    'export': eval(f"{file[:-3]}.plugin['export']")
                }
                logging.info(f"Loaded plugin [purple]{file}[/] ({this['version']}) by [purple]{this['author']}[/]", extra={"markup": True})
                for cmd in this['export']:
                    command_executors[cmd] = this['name'] # Add the command to the list of executors
            except Exception as e:
                console.print_exception()
                logging.error(f"Error while loading plugin {file}. See above.")
    with open('plugins.json', 'w') as f:
        json.dump({'command_executors': command_executors}, f, indent=4) # Save the executors to a file for the frontend
    return command_executors

# Load tasks and plugins
tasks = load_tasks(create_on_missing=True)
if tasks == -1:
    logging.critical("JSON file is corrupted")
    crash(-1)
elif tasks == -2:
    logging.critical("Wrong format in JSON file")
    crash(-2)

command_executors = load_plugins()

logging.info("Daemon started")
logging.info(f"Loaded {len(tasks)} tasks")
logging.info(f"Loaded {len(command_executors)} executors")

while True:
    # Wait for the next minute
    while datetime.datetime.now().second != 0:
        try:
            sleep(1)
        except KeyboardInterrupt:
            # Gracefully exit on Ctrl+C
            logging.warning("KeyboardInterrupt received, shutting down daemon...")
            exit(0)
            
    # Refresh tasks and plugins
    ntasks = load_tasks()
    if ntasks == None:
        logging.warning("Could not refresh tasks as tasks.json file is missing. Rerun the daemon to create it.")
    elif ntasks == -1:
        logging.warning("Could not refresh tasks as tasks.json file is corrupted")
    elif ntasks == -2:
        logging.warning("Could not refresh tasks as tasks.json file is in wrong format")
    elif ntasks != tasks:
        # If the tasks have changed, reload them
        logging.warning(f"Detect task changes, reloading.")
        logging.info(f"Loaded {len(ntasks)} tasks")
        tasks = ntasks
    command_executors = load_plugins(command_executors)
    
    # Get current time
    nowtime = datetime.datetime.now().strftime("%H:%M")
    logging.debug(f"Current time: {nowtime}")
    
    # Execute tasks
    for task in tasks:
        if task['time'] == nowtime:
            logging.info(f"Executing task id {task['id']}")
            if task['type'] == "command":
                # Execute the command
                try:
                    subprocess.run(task['command'], shell=True)
                except Exception as e:
                    console.print_exception()
                    logging.error(f"Error while executing task. see above.")
            elif task['type'] == "plugin":
                # Call the plugin
                try:
                    plug = command_executors[executor]
                    executor = task['command'].split(':')[0]
                    args = ' '.join(task['command'].split(':')[1:])
                    ret = eval(f"{plug}.{executor}({args})")
                    logging.info(f"Executor finished with return {ret}.")
                except Exception as e:
                    console.print_exception()
                    logging.error(f"Error while executing task. see above.")
    try:
        # Prevent multiple executions per second
        sleep(1)
    except KeyboardInterrupt:
        logging.warning("KeyboardInterrupt received, shutting down daemon...")
        exit(0)