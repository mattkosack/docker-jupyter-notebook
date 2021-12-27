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
        sys.exit('Could not open Docker.')

def start_container(name=None, path=None, new=True):
    """
    """
    cmds = {
        'new_named_dir': f'docker run --name {name} -p 8888:8888 -v {path}:/home/jovyan/work jupyter/datascience-notebook',
        'new_dir': f'docker run -p 8888:8888 -v {path}:/home/jovyan/work jupyter/datascience-notebook',
        'new_named_pwd': f'docker run --name {name} -p 8888:8888 -v "${{PWD}}":/home/jovyan/work jupyter/datascience-notebook',
        'new_pwd': f'docker run -p 8888:8888 -v "${{PWD}}":/home/jovyan/work jupyter/datascience-notebook',
        'named': f'docker start {name}'
    }

    if new:
        if name is not None and path is not None:
            # Name and Path given
            cmd = cmds['new_named_dir']
        elif name is None and path is not None:
            # Path is given
            cmd = cmds['new_dir']
        elif name is not None and path is None:
            # Name is given
            cmd = cmds['new_named_pwd']
        else:
            # Nothing is given
            cmd = cmds['new_pwd']
    else:
        # Old named container 
        cmd = cmds['named']

    try:
        process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, check=True)
        return process.stdout
    except:
        sys.exit("Could not start the container.")

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
        # Start a new one
        print("Starting a new docker container")
        output = start_container()

    elif num_args == 2:
        # Start and old named one
        output = start_container(sys.argv[1])

    elif num_args == 3 and sys.argv[1] == '-n':
        # output = start_new_named(sys.argv[2])
        print('nice')
    else:
        sys.exit("Too many arguments passed.")

    link = get_link(output)
    open_link(link)

if __name__=="__main__":
    go()