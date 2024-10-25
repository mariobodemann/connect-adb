###
#
# Script to run a developer machine server that can be connected to by an android phone using the script delivered by a GET request to this server.
# 
# Uses termux to run android local things. Could be an app, but isn't. :shrug:
#
# Process:
#
# 1. checkout this file on the developer machine
# 2. replace SERVER_ADDRESS down below with the servers ip address in the network the phone connects to too.
# 3. run server on local developer machine
# 4. install termux on Android developer phone
# 4.1. install termux-api on Android phone
# 4.2. install termux-widget on Android phone
# 5. install curl on Android phone
# 5.1. create folder `~/.shortcuts/` in termux home
# 6. curl the SERVER, saving response to .shortcuts: `curl $SERVER_ADDRESS > ~/.shortcuts/connect-adb
# 7. add termux widget to launcher: longpress on launcer background, scroll to termux, longpress on termux, move widget to where it needs to be, select 'connect-adb'.
# 8. enable wireless developer settings
# 9. open wireless developer settings
# 10. copy ip:port by longpressing on it and selecting copy
# 11. tap on 'connect-adb' in newly created widget
# 12. on developer machine confirm connection with `adb devices`.
# 13. trouble? Use adb connect tcp:12344 once on every phone while connected with usb
# 14. more trouble? file a ticket.
# 15. ....
# 16. profit
#
###

import http.server

SERVER_ADDRESS = "http://192.168.178.147:65535"

def reverseConnectFromPhoneToDevMachineToPhone():
    class StartADBConnectServerHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            """
            Inform user about which script to install in .shortcuts in termux....
            :return:
            """
            response = """#!/data/data/com.termux/files/usr/bin/env bash
# script to tell the developer machine to connect to the phone calling this script. Yolo.
#
# Put me under .shortcuts/ in termux and create a shortcut on desktop or something
#
# install missing commands if needed with `$0 install`

# update with dev machine ip address
server='SERVER_ADDRESS'

if [[ ${1} == "install" ]]; then
    command termux-clipboard-get 2> /dev/null && pkg install termux-api
    command curl 2> /dev/null && pkg install curl
    command jq 2> /dev/null && pkg install jq
fi

client="$(termux-clipboard-get)"
echo "(clipboard) client= ${client}."

if ! [[ "${client}" =~ ":" ]]; then
        client="$(termux-dialog text -t 'Enter Wireless Debug Address' -i 'ip:port' | jq -r .text)"
        echo "User dialog provided client '${client}'."

        if ! [[ "${client}" =~ ":" ]]; then
                termux-dialog confirm -t 'Failure' -i "'${client}' is an invalid IP." > /dev/null 2>&1
                exit
        fi
fi

result="$(curl --silent "${server}" -d "${client}")"
echo "${result}"

termux-dialog confirm -t 'Result' -i "${result}" > /dev/null 2>&1

""".replace("SERVER_ADDRESS", SERVER_ADDRESS)

            print(f"GET request from {self.client_address}.")

            self.wfile.write(
                f'HTTP/1.1 200 OK\n'
                f'Server: adb-yolo.py/0.0.01-SNAPSHOT\n'
                f'Content-Type: application/json; charset=UTF-8\n'
                f'Content-Length: {len(response)}\n'
                f'\n{response}'
                .encode('utf-8')
            )

        def do_POST(self):
            req_len = self.headers['Content-Length']
            request = self.rfile.read(int(req_len)).decode()

            print(f"Received {request} from {self.client_address}.")

            if ':' in request:
                response = call_adb(request)
                response_code = 200
            else:
                response = "Invalid payload. Please provide a body of 'ip:port' as POST payload.\n"
                response_code = 400

            self.wfile.write(
                f'HTTP/1.1 {response_code} OK\n'
                f'Server: adb-yolo.py/0.0.01-SNAPSHOT\n'
                f'Content-Type: text/plain charset=UTF-8\n'
                f'Content-Length: {len(response)}\n'
                f'\n{response}'
                .encode('utf-8')
            )

    def creator(a, b, c) -> http.server.BaseHTTPRequestHandler:
        return StartADBConnectServerHandler(a, b, c)

    http.server.HTTPServer(
        server_address=("", 65535),
        bind_and_activate=True,
        RequestHandlerClass=creator
    ).serve_forever()


def call_adb(request):
    import subprocess

    # start adb with that connectio
    ip, port = request.split(":")
    adb_command = ('adb', 'connect', f'{ip}:{port}',)

    process = subprocess.Popen(
        adb_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    process.wait()

    output = process.stdout.read().decode('utf-8')
    response = f"Output: {output}."
    return response


if __name__ == '__main__':
    reverseConnectFromPhoneToDevMachineToPhone()
