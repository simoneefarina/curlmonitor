#!/usr/bin/env python
import json
#imports
import subprocess
import typing
from mooncloud_driver import abstract_probe,atom,result,entrypoint

class Probe(abstract_probe.AbstractProbe):

    #Command to execute
    #-I: Fetch the headers only
    CMD_COMMAND = "curl -I {host}"

    #Result map
    RESULT_MAP = {
        result.INTEGER_RESULT_TRUE: {
            'pretty_result': "Test executed successfully",
            'base_extra_data': {}
        },
        result.INTEGER_RESULT_FALSE: {
            'pretty_result': "Error occurred during the test execution",
            'base_extra_data': {
                'Error': "{e}"
            }
        },
        result.INTEGER_RESULT_TARGET_CONNECTION_ERROR: {
            'pretty_result': "Target connection error",
            'base_extra_data': {
                'Error': "{e}"
            }
        },
        result.INTEGER_RESULT_INPUT_ERROR: {
            'pretty_result': "Input error",
            'base_extra_data': {
                'Error': "{e}"
            }
        },
        result.INTEGER_RESULT_MOON_CLOUD_ERROR: {
            'pretty_result': "Assertion failed",
            'base_extra_data': {
                'Error': "{e}"
            }
        }
    }

    # Checks the input are valid
    def check_input(self, inputs: None) -> bool :
        target = self.config.input ['config'] ['target']
        assert target is not None and target != "", "Input error: specify the target"

        self.target = target

        return True

    #Execute the command curl
    def execute_command(self, inputs: None) -> bool :
        target = self.target

        #Execution of the command
        sp = subprocess.run(self.CMD_COMMAND.format(host=target).split(" "), stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

        self.sp_returncode = sp.returncode

        #Casting the stderr from bytes to string in case of error
        if sp.returncode != 0:
            self.sp_stderr = sp.stderr.decode("utf-8")

        return True

    #Create the result based on the return code of the subprocess
    def set_output(self, inputs: None) -> bool :
        #Variable use to get the result from the RESULT_MAP
        result_int = int(0)

        #Input errors
        if self.sp_returncode == 1 or self.sp_returncode == 3:
            result_int = 3

        #Connection errors
        elif self.sp_returncode == 6 or self.sp_returncode == 7 or self.sp_returncode == 22 or self.sp_returncode == 28:
            result_int = 2

        #General error
        elif self.sp_returncode != 0:
            result_int = 1

        #Creation of the result
        result = self.RESULT_MAP.get(result_int)
        self.result.integer_result = result_int
        self.result.pretty_result = result['pretty_result']

        #Insert the Error in the result
        if result_int != 0:
            result['base_extra_data']['Error'] = self.sp_stderr
            self.result.base_extra_data['Error'] = self.sp_stderr

        return True

    def atoms(self) -> typing.Sequence[atom.AtomPairWithException]:
        return [
            atom.AtomPairWithException(self.check_input),
            atom.AtomPairWithException(self.execute_command),
            atom.AtomPairWithException(self.set_output)
        ]

if __name__ == '__main__':
    entrypoint.start_execution(Probe)