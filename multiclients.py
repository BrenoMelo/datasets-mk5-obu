import socket
import threading
import time
import IN
import random
from datetime import datetime

start = datetime.now()

def send_packets(client_id, event):
    try:
        MAX_RUN = 200
        now = datetime.now()
        print("Execution is starting at %s " % now)
        # Random ports
        rand_port_client = random.randint(1024,32768)
        rand_port_server = random.randint(1024,32768)

        # Create a socket for the client
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        client_socket.setsockopt(socket.SOL_SOCKET, IN.SO_BINDTODEVICE,str("wave-data"+'\0').encode('utf-8'))
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client_socket.bind(("",rand_port_client))

        # Create a socket for the server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server_socket.setsockopt(socket.SOL_SOCKET, IN.SO_BINDTODEVICE,str("wave-data"+'\0').encode('utf-8'))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server_socket.bind(("",rand_port_server))

        start_time = time.time()
        rand_duration = random.randint(5,30)
        count = 1
        i = 0
        while True:

                rand_stop = random.randint (10,20)
                current_time = time.time()
                run_time = current_time-start_time

                if run_time > rand_duration:

                        if count == MAX_RUN:
                                print("\t\tFinishing client %s " % client_id)
                                break
                        count += 1
                        print("\tClient %s is sleeping for %s seconds" % (client_id,rand_stop))
                        print("\t\tClient %s woke up" % client_id)
                        rand_duration = random.randint(5,30)
                        start_time = time.time()

                        client_socket.close()
                        server_socket.close()
                        time.sleep(rand_stop)
                        rand_port_client = random.randint(1024,32768)
                        rand_port_server = random.randint(1024,32768)

                        # Create a socket for the client
                        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                        client_socket.setsockopt(socket.SOL_SOCKET, IN.SO_BINDTODEVICE,str("wave-data"+'\0').encode('utf-8'))
                        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                        client_socket.bind(("",rand_port_client))

                        # Create a socket for the server
                        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                        server_socket.setsockopt(socket.SOL_SOCKET, IN.SO_BINDTODEVICE,str("wave-data"+'\0').encode('utf-8'))
                        #server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1512)
                        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                        server_socket.bind(("",rand_port_server))
                        i = 0
                else:

                        if i == 0:
                            print('Client ' + str(client_id) + ' is sending messages for ' + str(rand_duration) + ' seconds | counter ' + str(count))
                        rand_ept = round(random.random(),4)
                        rand_lat = round(1 + random.random(),3)
                        rand_lon = round(103 + random.random(),3)
                        rand_alt = round(random.uniform(33.000, 55.999),3)
                        rand_epx = 1
                        rand_epy = 1
                        rand_epv = 1
                        rand_track = 1
                        rand_speed = 1
                        rand_climb = 1
                        rand_eps = 1

                        out = {"class":"TPV",\
                                 "tag":"0x0107",    \
                                 "device":"/dev/ttymxc4",
                                 "mode":3,
                                 "time":"2023-09-15T08:56:24.000Z",
                                 "ept":rand_ept,
                                 "lat":rand_lat,
                                 "lon":rand_lon,
                                 "alt":rand_alt,
                                 "epx":rand_epx,
                                 "epy":rand_epy,
                                 "epv":rand_epv,
                                 "track":rand_track,
                                 "speed":rand_speed,
                                 "climb":rand_climb,
                                 "eps":rand_eps}
                        out = bytes(str(out).encode('utf-8'))

                        server_socket.sendto(out, ('<broadcast>',rand_port_client))

                        data, addr = client_socket.recvfrom(512)
                        i = 1


    except Exception as e:
        print("Client " + str(client_id) + " error: " + str(e))
    finally:
        client_socket.close()
        server_socket.close()

num_clients = 4
threads = []

for i in range(num_clients):
    event = threading.Event()
    client_thread = threading.Thread(target=send_packets, args=(i, event))
    client_thread.event = event  # Attach an event to each thread
    threads.append(client_thread)
    client_thread.start()

# Wait for all client threads to finish
for client_thread in threads:
    client_thread.join()

