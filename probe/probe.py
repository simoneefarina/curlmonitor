#!/usr/bin/env python
# imports
import typing
import copy

from urllib import request
from urllib.error import URLError, HTTPError
from mooncloud_driver import abstract_probe, atom, result, entrypoint


class Probe(abstract_probe.AbstractProbe):

    # Creation of the result map
    RESULT_MAP = {
        result.INTEGER_RESULT_TRUE: {
            'pretty_result': "Test executed successfully",
            'base_extra_data': {}
        },
        result.INTEGER_RESULT_FALSE: {
            'pretty_result': "An error occurred during test execution",
            'base_extra_data': {
                'error': "{e}"
            }
        },
        result.INTEGER_RESULT_TARGET_CONNECTION_ERROR: {
            'pretty_result': "Failed to connect to the target",
            'base_extra_data': {
                'error': "{e}"
            }
        },
        result.INTEGER_RESULT_MOON_CLOUD_ERROR: {
            'pretty_result': "An unexpected error occurred",
            'base_extra_data': {
                'error': "{e}"
            }
        }
    }

    def __init__(self):
        super().__init__()
        self.error = None
        self.result_code = None
        self.target = None

    # Set the target
    def set_input(self, inputs: None) -> bool:
        target = self.config.input['config']['target']

        self.target = target

        return True

    # Execute the HTTP request to the target
    def execute_request(self, inputs: None) -> bool:
        target = self.target

        try:
            response = request.urlopen(target, timeout=10)
            self.result_code = response.getcode()
        except HTTPError as e:
            self.result_code = e.code
            self.error = str(e)
        except URLError as e:
            self.result_code = result.INTEGER_RESULT_TARGET_CONNECTION_ERROR
            self.error = str(e.reason)
        except Exception as e:
            self.result_code = result.INTEGER_RESULT_MOON_CLOUD_ERROR
            self.error = str(e)

        return True

    # Create the result
    def create_result(self, inputs: None) -> result:

        if self.result_code == result.INTEGER_RESULT_TARGET_CONNECTION_ERROR:
            result_integer = result.INTEGER_RESULT_TARGET_CONNECTION_ERROR
        elif self.result_code == result.INTEGER_RESULT_MOON_CLOUD_ERROR:
            result_integer = result.INTEGER_RESULT_MOON_CLOUD_ERROR
        elif self.result_code != 200:
            result_integer = result.INTEGER_RESULT_FALSE
        else:
            result_integer = result.INTEGER_RESULT_TRUE

        result_obj = self.RESULT_MAP.get(result_integer)
        base_extra_data = copy.deepcopy(result_obj['base_extra_data'])
        if result_integer != result.INTEGER_RESULT_TRUE:
            base_extra_data['error'] = base_extra_data['error'].format(e=self.error)

        self.result.integer_result = result_integer
        self.result.pretty_result = result_obj['pretty_result']
        self.result.base_extra_data = base_extra_data

        return True

    def atoms(self) -> typing.Sequence[atom.AtomPairWithException]:
        return [
            atom.AtomPairWithException(self.set_input),
            atom.AtomPairWithException(self.execute_request),
            atom.AtomPairWithException(self.create_result)
        ]


if __name__ == '__main__':
    entrypoint.start_execution(Probe)
