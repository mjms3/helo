import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import daemon
import random
import math as m


from esp.esp import ShortestPathFinder
from sandbox import gb_map

DEFAULT_PORT_NUMBER = 49152

RESPONSE_SUCCESS = 200
RESPONSE_BAD_REQUEST = 400

POINT_TOLERANCE = 1e-6

HELICOPTER_MIN_SPEED = 80
HELICOPTER_MAX_SPEED = 250


class ESPRequestsHandler(BaseHTTPRequestHandler):
    log_file = open('server_logs.log', 'w')

    path_finder = ShortestPathFinder(gb_map.vertices, gb_map.triangles,
                                     triangle_weights=[1 + 5 * random.random() for _ in gb_map.triangles])

    def log_message(self, format_string, *args):
        self.log_file.write("%s - - [%s] %s\n" %
                            (self.client_address[0],
                             self.log_date_time_string(),
                             format_string % args))
        self.log_file.flush()

    def _get_and_validate_query(self, payload):
        start = payload.pop('start')
        end = payload.pop('end')
        speed = payload.pop('speed')
        if payload:
            raise ValueError('Unexpected arguments in the payload.')

        if m.fabs(start[0] - end[0]) < POINT_TOLERANCE and m.fabs(start[1] - end[1]) < POINT_TOLERANCE:
            raise ValueError('Start point is too close to the end point.')

        if not (HELICOPTER_MIN_SPEED < speed < HELICOPTER_MAX_SPEED):
            raise ValueError('Helicopter speed not within expected bounds')
        return start, end, speed

    def do_POST(self):

        try:
            data_stream = self.rfile.read(int(self.headers['Content-Length']))
            payload = json.loads(data_stream.decode())
            start, end, speed = self._get_and_validate_query(payload)
            json_output = self.path_finder.calculate_path_in_json_format(start, end, speed, subdivisions=6)
        except Exception as ex:
            exception_string = str(ex)
            self._return_error(exception_string)
            return
        self._return_success(json_output)

    def _return_success(self, payload):
        self.send_response(RESPONSE_SUCCESS)
        self.send_header('Content-type'.encode(), 'application/json'.encode())
        self.end_headers()
        self.wfile.write(payload.encode())

    def _return_error(self, exception_string):
        self.send_response(RESPONSE_BAD_REQUEST)
        self.send_header('Content-type'.encode(), 'application/json'.encode())
        self.end_headers()
        return_payload = {'Details': 'Data validation failed with error: {}'.format(exception_string).encode()}
        self.wfile.write(json.dumps(return_payload).encode())


if __name__ == '__main__':
    import argparse

    random.seed(1234)
    parser = argparse.ArgumentParser(description='Euclidean Shortest Pathfinder for Helo. '
                                                 'This program launches a webserver that responds to POST requests.')
    parser.add_argument('-D', '--daemon', dest='daemon', help='Launch the process as a daemon.', action='store_true',
                        default=False)
    parser.add_argument('-p', '--port', dest='port', help='Port to launch the server on', default=DEFAULT_PORT_NUMBER)
    args = parser.parse_args()

    server = HTTPServer(('', args.port), ESPRequestsHandler)

    if args.daemon:
        daemon_context = daemon.DaemonContext()
        daemon_context.files_preserve = [server.fileno(), ESPRequestsHandler.log_file]

        with daemon_context:
            server.serve_forever()
    else:
        server.serve_forever()
