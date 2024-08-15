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

        request.urlopen(target, timeout=10)

        return True

    # Create the result in case of success
    def request_success(self, inputs: None) -> result:
        result_success = self.build_result(result.INTEGER_RESULT_TRUE)

        self.result.integer_result = result_success.integer_result
        self.result.pretty_result = result_success.pretty_result
        self.result.base_extra_data = result_success.base_extra_data

        return True

    # Create the result in case of an error
    def request_error(self, e):
        error = ""

        if isinstance(e, HTTPError):
            result_integer = result.INTEGER_RESULT_FALSE
            error = str(e)
        elif isinstance(e, URLError):
            result_integer = result.INTEGER_RESULT_TARGET_CONNECTION_ERROR
            error = str(e.reason)
        else:
            result_integer = result.INTEGER_RESULT_MOON_CLOUD_ERROR
            error = str(e)

        return self.build_result(result_integer, error)

    # Build the result
    def build_result(self, result_code: int, error: str = "") -> result.Result:
        result_obj = self.RESULT_MAP.get(result_code)
        base_extra_data = copy.deepcopy(result_obj['base_extra_data'])

        if 'error' in base_extra_data:
            base_extra_data['error'] = base_extra_data['error'].format(e=error)

        return result.Result(
            integer_result=result_code,
            pretty_result=result_obj['pretty_result'],
            base_extra_data=base_extra_data
        )

    def atoms(self) -> typing.Sequence[atom.AtomPairWithException]:
        return [
            atom.AtomPairWithException(self.set_input),
            atom.AtomPairWithException(forward=self.execute_request, forward_captured_exceptions=[
                atom.PunctualExceptionInformationForward(
                    exception_class=HTTPError,
                    action=atom.OnExceptionActionForward.STOP,
                    result_producer=self.request_error
                ),
                atom.PunctualExceptionInformationForward(
                    exception_class=URLError,
                    action=atom.OnExceptionActionForward.STOP,
                    result_producer=self.request_error
                ),
                atom.PunctualExceptionInformationForward(
                    exception_class=Exception,
                    action=atom.OnExceptionActionForward.STOP,
                    result_producer=self.request_error
                ),
            ]),
            atom.AtomPairWithException(self.request_success)
        ]


if __name__ == '__main__':
    entrypoint.start_execution(Probe)
