from subprocess import PIPE, call, Popen
import shlex


def _run_background_process(command_line):
    """This method runs external program using command line interface.

    Returns:
         stdout,stdin: Of executed program.
    """

    args = shlex.split(command_line, posix=False)
    '''process = run(args, stdout=PIPE, stderr=PIPE, shell=True, check=True)
    stdout = process.stdout
    stderr = process.stderr'''

    process = Popen(args, stdout=PIPE, stderr=PIPE)
    process.wait()
    stdout = process.stdout.read().decode().strip()
    stderr = process.stderr.read().decode().strip()

    return stdout, stderr

