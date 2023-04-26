import subprocess
from termcolor import colored

# Run the Git command
result = subprocess.run("git pull", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Check the return code to see if the command was successful
if result.returncode == 0:
    # Print a success message in green text
    print(colored("Update successful!", "green"))
else:
    # Print the output of the command in red text
    print(colored("Error updating repository:\n" + result.stderr.strip(), "red"))
