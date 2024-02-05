import os
import json
from datetime import datetime

from rich import print
from rich.markup import escape
from rich.table import Table

args = os.sys.argv

def print_usage():
    # Print usage
    print(f"[blue bold]Usage:[/] frontend.py <[purple]args[/]>")
    print(f"")
    print(f"[blue bold]Arguments:[/]")
    print(f"  [purple bold]help[/] - Show this help message")
    print(f"  [purple bold]add[/] - Add a new task")
    print(f"  [purple bold]remove[/] - Remove a task")
    print(f"  [purple bold]list[/] - List all tasks")

if len(args) == 1:
    # No arguments provided
    print(f"[red bold]Error:[/red bold] No arguments provided, use [blue bold]frontend.py help[/] for help.")
    exit(1)

if args[1] == "help":
    print_usage()
    exit(0)
elif args[1] == "add":
    if len(args) < 3:
        # Not enough arguments
        print(f"[red bold]Error:[/red bold] Task details must be provided.")
        print(f"")
        print(f"[blue bold]Usage:[/] frontend.py add <[purple]time[/]> <[purple]command|plugin>")
        print(f"- [purple]time[/] must be in the format [blue bold]HH:MM[/].")
        exit(1)
    time = args[2]
    try:
        # Check if time is in the correct format
        atetime.strptime(time, "%H:%M")
    except ValueError:
        print(f"[red bold]Error:[/red bold] Invalid time format. Time must be in the format [blue bold]HH:MM[/].")
        exit(1)
    tasktype = args[3]
    if tasktype == 'command':
        # Get the command
        cmd = input("Enter the command\n> ")
    elif tasktype == 'plugin':
        # Check if the plugin is in the list of executors
        with open("plugins.json", "r") as f:
            plugins = json.load(f)["command_executors"]
        if executor not in plugins.keys():
            print(f"[red bold]Error:[/red bold] Executor '{executor}' invaild. Initalize the plugin by running daemon once.")
            exit(1)
        # Get the plugin and arguments
        plug = input("Enter the plugin/executor\n> ")
        args = input("Enter the arguments of the plugin (Use ',' to seperate)\n> ")
        cmd = f"{plug}:{args}"
    # Print task details
    print(f"[bold]Adding a new task:[/]")
    print(f"  [blue bold]Time:[/] {time}")
    print(f"  [blue bold]Type:[/] {tasktype}")
    print(f"  [blue bold]Command/Plug:[/] '{cmd}'")
    # Add the task to file
    with open("tasks.json", "r") as f:
        tasks = json.load(f)["tasks"]
    if len(tasks) == 0:
        id = 1
    else:
        id = tasks[-1]["id"] + 1
    tasks.append({"id":id,"time":time,"command":cmd, "type":tasktype})
    with open("tasks.json", "w") as f:
        json.dump({"tasks":tasks}, f)
    print(f"[green bold]Task added successfully.[/] (ID: {id})")
    exit(0)
elif args[1] == "remove":
    if len(args) < 3:
        # Not enough arguments
        print(f"[red bold]Error:[/red bold] Task ID must be provided. Use [blue bold]frontend list[/] to get the ID of the task to remove.")
        print(f"")
        print(f"[blue bold]Usage:[/] frontend.py remove <[purple]id[/]>")
        exit(1)
    id = int(args[2])
    # Remove the task from file
    with open("tasks.json", "r") as f:
        tasks = json.load(f)["tasks"]
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            with open("tasks.json", "w") as f:
                json.dump({"tasks":tasks}, f)
            print(f"[green bold]Task removed successfully.[/] (ID: {id})")
            exit(0)
    print(f"[red bold]Error:[/red bold] Task with ID {id} not found.")
    exit(1)
elif args[1] == "list":
    with open("tasks.json", "r") as f:
        tasks = json.load(f)["tasks"]
    if len(args) > 2:
        if args[2] == "time":
            tasks.sort(key=lambda task: task["time"])
        elif args[2] == "id":
            tasks.sort(key=lambda task: task["id"])
        else:
            print(f"[red bold]Error:[/red bold] Invalid sorting method. Use [blue bold]time[/] [grey](default)[/] or [blue bold]id[/] followed.")
            exit(1)
    tasks.sort(key=lambda task: task["time"])
    # Construct the rich table
    table = Table(title="Tasks")
    table.add_column("ID", style="blue bold")
    table.add_column("Time", style="blue bold")
    table.add_column("Command", style="blue bold")
    for task in tasks:
        table.add_row(str(task["id"]), task["time"], task["command"])
    # Print the table
    print(table)
    exit(0)
else:
    print(f"[red bold]Error:[/red bold] Invalid argument '{' '.join(args[1:])}'. Use [blue bold]frontend.py help[/] for help.")
    exit(1)