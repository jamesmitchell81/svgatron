import sys, os, csv, json

"""
J(i) = J(i - 1) + ( |D(i - 1, i)| - J(i - 1)) / 16

D(i, j) = (Rj - Ri) - (Sj - Si) = (Rj - Sj) - (Ri - Si)

Si = timestamp from packet i, sent = rtp.timestamp
Ri = time of arrival for packet i, recieved = frame.time_epoch
"""

"""
TODO: record filename/tc parameters.
filename.split("-")
"""

"""
TODO: capture summary.
- Average
- Max
- Average max

- graphs
"""

ext = ".tab"
directory = "./data"

hertz = 8000
second = 1.0
ms = 1000

def collect_data():

    data = {}
    calls = {}

    for filename in os.listdir(directory):

        if filename.endswith(ext):
            mode = 'rb'
            file_to_open = directory + "/" + filename

            filename = filename.split(".")
            filename = filename[0]
            params = filename.split("-")

            date = "-".join(params[len(params) - 3: len(params)])
            interface = "-".join(params[len(params) - 5: len(params) - 3])
            print interface

            with open(file_to_open, mode) as file:

                reader = csv.DictReader(file, delimiter='\t')
                
                print "Collecting SIP..."
                for row in reader:
                    if row['udp.srcport'] == "5060":
                        
                        # SIP INVITE
                        if row['sip.Method'] == "INVITE":
                            id = row['sip.Call-ID']
                            if id not in calls:
                                call = { 'packets': {} }
                                calls[id] = call
                                call['id'] = id

                                call['from'] = row['ip.src']
                                call['to'] = row['ip.dst']
                                call['dst-port'] = row['sdp.media.port']

                        # SIP OK
                        if row['sip.CSeq.method'] == "INVITE" and row['sip.Status-Code'] == "200":
                            id = row['sip.Call-ID']
                            call = calls[id]
                            call['src-port'] = row['sdp.media.port']
                            udp_ports = call['dst-port'] + "-" + call['src-port']

                            if interface not in call['packets']:
                                call['packets'][interface] = {}
                                call['packets'][interface]['forward'] = []
                                call['packets'][interface]['reverse'] = []

                            data[udp_ports] = call

                file.seek(0)
                
                print "Collecting RTP..."
                next(reader)
                for row in reader:
                    forward = row['udp.dstport'] + "-" + row['udp.srcport']
                    reverse = row['udp.srcport'] + "-" + row['udp.dstport']

                    if forward in data or reverse in data:
                        packet = {}
                        packet['from'] = row['ip.src']
                        packet['to'] = row['ip.dst']
                        packet['seq'] = int(row['rtp.seq'])
                        packet['rtp-timestamp'] = float(row['rtp.timestamp'])
                        packet['frame-arrival'] = float(row['frame.time_epoch'])
                        packet['delta'] = float(row['frame.time_delta'])

                    if forward in data:
                        data[forward]['packets'][interface]['forward'].append(packet)

                    if reverse in data:
                        data[reverse]['packets'][interface]['reverse'].append(packet)

    call_summary = {
        'calls': []
    }

    print "Calculating Jitter..."
    for udp_ports in data:
        interfaces = data[udp_ports]['packets']

        max = 0
        min = 1

        call = {}
        call['ip-src'] = data[udp_ports]['from']
        call['ip-dst'] = data[udp_ports]['to']
        call_summary['calls'].append(call)

        for interface in interfaces:

            call[interface] = {}

            for direction in interfaces[interface]:
                
                call[interface][direction] = {}
                call[interface][direction]['jitter'] = []
                call[interface][direction]['frame-arrival'] = []

                packets = interfaces[interface][direction]
                packets_count = len(packets)

                packets[0]['inter-arrival-time'] = 0
                packets[0]['jitter'] = 0

                for packet in range(1, packets_count):
                    prev_packet = packets[packet - 1]
                    this_packet = packets[packet]

                    unit = (second / hertz)
                    sent_variance_ms = (this_packet['rtp-timestamp'] * unit) - (prev_packet['rtp-timestamp'] * unit)
                    received_variance_ms = this_packet['frame-arrival'] - prev_packet['frame-arrival']
                    packets[packet]['sent-variance-ms'] = sent_variance_ms
                    packets[packet]['received-variance-ms'] = received_variance_ms

                    # D(i, j) = (Rj - Ri) - (Sj - Si) = (Rj - Sj) - (Ri - Si)
                    packets[packet]['inter-arrival-time'] = (received_variance_ms) - (sent_variance_ms)
                    # J(i) = J(i - 1) + ( |D(i - 1, i)| - J(i - 1)) / 16
                    packets[packet]['jitter'] = prev_packet['jitter'] + ((abs(packets[packet]['inter-arrival-time']) - prev_packet['jitter']) / 16)
                    packets[packet]['jitter-ms'] = "%.6f" % (packets[packet]['jitter'] * ms)

                    call[interface][direction]['jitter'].append(packets[packet]['jitter'] * ms)
                    call[interface][direction]['frame-arrival'].append(this_packet['frame-arrival'])

                    if packets[packet]['jitter'] > max:
                        max = packets[packet]['jitter']

                    if packets[packet]['jitter'] < min and packets[packet]['jitter'] > 0:
                        min = packets[packet]['jitter']


        call['max-jitter-ms'] = max * ms
        call['min-jitter-ms'] = min * ms if min != 1 else 0

    with open('data.json', 'w') as out:
        json.dump(data, out, indent = 2)

    with open('call-summary.json', 'w') as out:
        json.dump(call_summary, out, indent = 2)

    return call_summary

# if __name__ == '__main__':
#     sys.exit(main())