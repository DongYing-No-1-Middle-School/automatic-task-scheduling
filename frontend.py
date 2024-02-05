import os
import json

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
    if len(args) < 4:
        # Not enough arguments
        print(f"[red bold]Error:[/red bold] Task details must be provided.")
        print(f"")
        print(f"[blue bold]Usage:[/] frontend.py add <[purple]time[/]> (-p) <[purple]command|plugin[green bold]:[/]args[/]>")
        print(f"- [purple]time[/] must be in the format [blue bold]HH:MM[/].")
        print(f"- [purple]-p[/] is an optional argument to run the command with [blue bold]plugin executor[/].")
        exit(1)
    time = args[2]
    if len(time) != 5 or time[2] != ":":
        # Simple time format check
        print(f"[red bold]Error:[/red bold] Invalid time format. Time must be in the format [blue bold]HH:MM[/].")
        exit(1)
    if args[3] == "-p":
        # Type of task is plugin
        tasktype = "plugin"
        command = " ".join(args[4:])
        executor = command.split(":")[0]
        args = command.split(":")[1]
        with open("plugins.json", "r") as f:
            plugins = json.load(f)["command_executors"]
        if executor not in plugins.keys():
            print(f"[red bold]Error:[/red bold] Executor '{executor}' invaild.")
            exit(1)
    else:
        # Type of task is command
        command = " ".join(args[3:])
        tasktype = "command"
    # Print task details
    print(f"[bold]Adding a new task:[/]")
    print(f"  [blue bold]Time:[/] {time}")
    print(f"  [blue bold]Type:[/] {tasktype}")
    print(f"  [blue bold]Command:[/] '{command}'")
    with open("tasks.json", "r") as f:
        tasks = json.load(f)["tasks"]
    if len(tasks) == 0:
        id = 1
    else:
        id = tasks[-1]["id"] + 1
    tasks.append({"id":id,"time":time,"command":command, "type":tasktype})
    with open("tasks.json", "w") as f:
        json.dump({"tasks":tasks}, f)
    print(f"[green bold]Task added successfully.[/] (ID: {id})")
    exit(0)
elif args[1] == "remove":
    if len(args) < 3:
        # Not enough arguments
        print(f"[red bold]Error:[/red bold] Task ID must be provided.")
        print(f"")
        print(f"[blue bold]Usage:[/] frontend.py remove <[purple]id[/]>")
        exit(1)
    id = int(args[2])
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
    table = Table(title="Tasks")
    table.add_column("ID", style="blue bold")
    table.add_column("Time", style="blue bold")
    table.add_column("Command", style="blue bold")
    for task in tasks:
        table.add_row(str(task["id"]), task["time"], task["command"])
    print(table)
    exit(0)
else:
    print(f"[red bold]Error:[/red bold] Invalid argument '{' '.join(args[1:])}'. Use [blue bold]frontend.py help[/] for help.")
    exit(1)