import asyncio
import sys
import logging
import numpy as np
import pandas as pd
from IPython.display import display

clients = {}  # task -> (reader, writer)

log = logging.getLogger(__name__)

#load data
dt_pers = pd.read_csv("persons.csv", sep='\t', header=0, index_col=False)
dt_rec = pd.read_csv("records.csv", sep='\t', header=0, index_col=False)
dt_msg = pd.read_csv("therapy.csv", sep='\t', header=0, index_col=False)
dt_rec = dt_rec.convert_dtypes()
dt_pers = dt_pers.convert_dtypes()
dt_msg = dt_msg.convert_dtypes()

dt_rec['datetime'] = pd.to_datetime(dt_rec['datetime'], format="%Y-%m-%dT%H:%M:%S")
dt_msg['datetime'] = pd.to_datetime(dt_msg['datetime'], format="%Y-%m-%dT%H:%M:%S")

#strID = "ID 110|2013-01-01T05:00:00|120|80|60|9"
#strMSG = "MSG 110|2013-01-01T05:00:00|test 100"
#str = strMSG
#display(str)

def accept_client(client_reader, client_writer):
    task = asyncio.Task(handle_client(client_reader, client_writer))
    clients[task] = (client_reader, client_writer)

    def client_done(task):
        del clients[task]
        client_writer.close()
        log.info("End Connection")

    log.info("New Connection")
    task.add_done_callback(client_done)


@asyncio.coroutine
def handle_client(client_reader, client_writer):
    # send a hello to let the client know they are connected
    client_writer.write("HELLO\n".encode())

    # give client a chance to respond, timeout after 10 seconds
    data = yield from asyncio.wait_for(client_reader.readline(),
                                       timeout=360.0)

    if data is None:
        log.warning("received None")
        return
        
    sdata = data.decode().rstrip()
    log.info("Received %s", sdata)
    if sdata != "READY":
        log.warning("Expected READY, received '%s'", sdata)
        return
     
    while True:
        # wait for input from client
        data = yield from asyncio.wait_for(client_reader.readline(),
                                           timeout=3600.0)
        if data is None:
            log.warning("received None")
            continue
            
        sdata = data.decode().rstrip()
        log.info("Received %s", sdata)
        
        if sdata.upper() == 'BYE':
            client_writer.write("BYE\n".encode())
            break    
            
        if str[0:3].upper() == "MSG":
            ss = [x for x in str[4:].split('|')]
            df = pd.DataFrame([{'id' : int(ss[0]), 'datetime' : datetime.strptime(ss[1], "%Y-%d-%mT%H:%M:%S"), 'therapy' : ss[2]}])
            dt_msg = pd.concat([dt_msg, df], ignore_index=True, sort=False)
        elif str[0:3].upper() == "REC":
            ss = [x for x in str[4:].split('|')]
            df = pd.DataFrame([{'id' : int(ss[0]), 'datetime' : datetime.strptime(ss[1], "%Y-%d-%mT%H:%M:%S"), 'sys' : int(ss[2]), 'dia' : int(ss[3]), 'pulse' : int(ss[4]), 'exercise' : int(ss[5])}])
            dt_rec = pd.concat([dt_rec, df], ignore_index=True, sort=False)
        elif str[0:2].upper() == "ID":
            ss = [x for x in str[3:].split('|')]
            df = pd.DataFrame([{'id' : int(ss[0]), 'sex' : int(ss[1]), 'height' : int(ss[2]), 'weight' : int(ss[3]), 'snils' : ss[4]}])
            dt_rec = pd.concat([dt_rec, df], ignore_index=True, sort=False)
        elif str[0:7].upper() == "GET_MSG":
            ss = int(str[8:])
            df = dt_msg.loc[dt_msg['id'] == ss]
            client_writer.write("GET_MSG ".encode() + df.to_string(header=False, index=False).encode())
        elif str[0:7].upper() == "GET_PER": 
            ss = int(str[8:])
            df = dt_pers.loc[dt_pers['id'] == ss]
            client_writer.write("GET_PER ".encode() + df.to_string(header=False, index=False).encode())
        elif str[0:7].upper() == "GET_REC": 
            ss = int(str[8:])
            df = dt_rec.loc[dt_rec['id'] == ss]
            client_writer.write("GET_REC ".encode() + df.to_string(header=False, index=False).encode())
        else:
            log.warning("Expected type ID, MSG, REC, GET_MSG, GET_PER, GET_REC - received '%s'", str)

def main():
    loop = asyncio.get_event_loop()
    f = asyncio.start_server(accept_client, host=None, port=8502)
    loop.run_until_complete(f)
    loop.run_forever()

    #save data on exit
    dt_pers.to_csv("persons.csv", sep='\t', index=False)
    dt_rec.to_csv("records.csv", sep='\t', index=False)
    dt_msg.to_csv("therapy.csv", sep='\t', index=False)


if __name__ == '__main__':
    log = logging.getLogger("")
    formatter = logging.Formatter("%(asctime)s %(levelname)s " +
                                  "[%(module)s:%(lineno)d] %(message)s")
    # setup console logging
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(formatter)
    log.addHandler(ch)
    main()
    