import subprocess
import sys
import time

# TODO: 
# Error checking if name already exists.
# Check that they start at all
# Support creation at different path
# Refactor creation, definitely have some redundant code

def docker_running():
    """
    Return whether docker stats have any info.

    The &> /dev/null silences the docker errors.
    See the docker stats doc:
        https://docs.docker.com/engine/reference/commandline/stats/
    """
    process = subprocess.run("(! docker stats --no-stream &> /dev/null)", shell=True, stdout=subprocess.PIPE)
    return process.returncode


def start_docker():
    """
    Start the docker daemon if not already running.
    """
    try:
        process = subprocess.run("open /Applications/Docker.app", shell=True, stdout=subprocess.PIPE, check=True)
        return process.stdout
    except:
        print('Could not open docker.')

def start_new(path=None):
    """
    """
    cmd = 'docker run -p 8888:8888 -v "${PWD}":/home/jovyan/work jupyter/datascience-notebook'
    try:
        process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, check=True)
        return process.stdout
    except:
        print("Could not start a new container")

def start_named(name):
    """
    Start the passed docker container name.
    """
    container_id = get_container_id(name)
    cmd = f'docker start -a {container_id}'
    try:
        process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, check=True)
        return process.stdout
    except:
        print("Could not start the named container.")

# TODO: This one 
def start_new_named(name):
    """
    Start a new container with the given name.
    """
    cmd = f'docker run --name {name} -p 8888:8888 -v "${{PWD}}":/home/jovyan/work jupyter/datascience-notebook'
    try:
        process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, check=True)
        return process.stdout
    except:
        print("Could not start the newly named container.")


def get_container_id():
    """
    """
    return ...

def get_link():
    """
    Get the link from the docker prompts.
    """
    pass

def open_link():
    """
    Open the link passed.
    """
    pass

def go():

    if not docker_running():
        print('Starting Docker')
        start_docker()

    while not docker_running():
        print('Waiting for Docker to run...')
        time.sleep(2)

    # Check the arguments
    num_args = len(sys.argv)
    if num_args == 1:
        print("Starting a new docker container at TODO")
        output = start_new()

    elif num_args == 2:
        output = start_named(sys.argv[1])

    elif num_args == 3 and sys.argv[1] == '-n':
        # output = start_new_named(sys.argv[2])
        print('nice')
    else:
        sys.exit("Too many arguments passed.")

    link = get_link(output)
    open_link(link)

if __name__=="__main__":
    go()