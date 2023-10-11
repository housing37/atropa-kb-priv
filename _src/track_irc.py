__fname = 'track_irc'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#------------------------------------------------------------#
#   IMPORTS                                                  #
#------------------------------------------------------------#
import sys, os, time
from datetime import datetime
import requests, json
import socket, threading
import db_controller as dbc

# dt format = 'Oct 08' & 'Oct 09'
import maria_irc_100923, maria_irc_100923_tot

# dt format = '[4:37am]' & '[12:37pm]'
import maria_irc_100823, maria_irc_100823_2, maria_irc_100923_2
import maria_irc_101023_0, maria_irc_101023_1

#from web3 import Web3
#import inspect # this_funcname = inspect.stack()[0].function
#parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(parent_dir) # import from parent dir of this file

#------------------------------------------------------------#
#   GLOBALS
#------------------------------------------------------------#

#------------------------------------------------------------#
#   FUNCTION SUPPORT                                         #
#------------------------------------------------------------#
# Function to send PING commands every 400 seconds
#def send_ping_commands():
#    while True:
#        ping = '... keep-alive PING'
#        print('['+get_time_now()+'] '+ping)
#        irc.send(bytes("PING :keep-alive\r\n", "UTF-8"))
#        #time.sleep(400)
#        wait_sleep(1, b_print=True) # sleep 'wait_sec'

# Function to listen for incoming messages
#def listen_for_messages():
def track_msgs(server, port, nick='guest50040', channel='#test', pw=''):
    # Create a socket connection to the IRC server
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((server, port))

    # Send the IRC handshake and join the channel
    irc.send(bytes(f"USER {nick} 0 * :{nick}\r\n", "UTF-8"))
    irc.send(bytes(f"NICK {nick}\r\n", "UTF-8"))
    irc.send(bytes(f"JOIN {channel} {pw}\r\n", "UTF-8"))

    while True:
        # data = ":r_!~r@ec2-18-188-176-66.us-east-2.compute.amazonaws.com PRIVMSG #test :te"
        data = irc.recv(2048).decode("UTF-8")
        str_print = str_time = usr = usr_full = usr_loc = msg = msg_type = 'nil_str'
        if not data:
            break

        # check for ping
        if data.split()[0] == "PING":
            str_print = '['+get_time_now()+'] '+data.rstrip()+' ... PONG\n'
            print(str_print)
            irc.send(bytes(f"PONG {data.split()[1]}\r\n", "UTF-8"))
        else:
            # Print formatted msg to the console
            #str_print, str_time, usr, msg = parse_msg_string(data, channel)
            str_print, str_time, usr, usr_full, usr_loc, msg, msg_type = parse_msg_string(data, channel)
            print(str_print)
            
            # update db
            keyVals = { 1:server, 2:port, 3:nick, 4:channel, 5:str_print, 6:str_time,
                        7:usr_full, 8:usr_loc, 9:usr, 10:msg, 11:msg_type, 12:data }
            lst_db_return, success = db_add_log(keyVals)
        
        if 'mariarahel' in usr:
            pass # TODO: notify admin

    # Close the IRC connection when done
    irc.close()
    
def db_add_log(keyVals):
    #if kPin in keyVals: del keyVals[kPin]
    db_return = dbc.exe_stored_proc(-1, 'irc_ADD_LOG', keyVals)
    bErr = 'status' not in db_return[0] or db_return[0]['status'] != 'success'
    if bErr:
        print('\n\n*** DB ERROR ***', " _ bErr from 'irc_ADD_LOG'", f"info:\n {db_return}", '*** DB ERROR ***\n', sep='\n')
        return db_return, False
    return db_return, True
    
def parse_msg_string(data, channel, flag=-1):
    # format user msg
    #str_msg_start = '!-'+nick+'@'
    str_result = str_time = usr = usr_full = usr_loc = msg = msg_type = 'nil_parse'
    
    # run w/ maria_irc_100923, maria_irc_100923_tot
    if 'Oct 08' in data or 'Oct 09' in data:
        # ex: data = 'Oct 08 01:11:25 <PassportPowell>	Hi everyone'
        parts = data.split()
        day = parts[1]
        time = parts[2]
        usr = parts[3].replace('<','').replace('>','')
        msg = ' '.join(parts[4:len(parts)])
        
        str_print = channel+'  <'+usr+'>    '+msg
        str_time = '2023-10-08 ' if day == '08' else '2023-10-09 '
        str_time = str_time + time
        str_result = '['+str_time+'] '+str_print

    # run w/ maria_irc_100823, maria_irc_100823_2, maria_irc_100923_2
    # run w/ maria_irc_101023_0, maria_irc_101023_1
    elif data.startswith('['):
        # ex: data = '[4:41pm] mariarahel: reached zero confidence in doge'
        # ex: data = '[3:42pm] pulseperza joined the chat room.'
        parts = data.split()
        time = parts[0].replace('[','').replace(']','')
        if 'am' in time:
            time = time.replace('am','')
            if time.index(':') == 1:
                time = '0'+time
        elif 'pm' in time:
            time = time.replace('pm','')
            if time[0:2] == '12': # handle special case 12pm
                time = "00"+time[2:]
            hr = int(time[0:time.index(':')]) + 12
            time = f"{hr}{time[time.index(':'):]}"
        else:
            time = 'ERROR ... no am or pm found in time'
            
        usr = parts[1].replace(':','')
        msg = ' '.join(parts[2:len(parts)])
        
        str_print = channel+'  <'+usr+'>    '+msg
        if flag == 0: str_time = '2023-10-08 '+time # run w/ maria_irc_100823, maria_irc_100823_2
        if flag == 1: str_time = '2023-10-09 '+time # run w/ maria_irc_100923_2
        if flag == 2: str_time = '2023-10-10 '+time # run w/ maria_irc_101023_0, maria_irc_101023_1
        str_result = '['+str_time+'] '+str_print
        
    # check for users joing / leaving channel
    elif 'join' in data.lower() or 'part' in data.lower():
        str_time = get_time_now()
        str_result = '['+str_time+'] '+data
    
    # check for msg format
    #elif (data[0] == ':' and data.find(str_msg_start) > -1):
    #    usr = data[1:data.index(str_msg_start):1]
    #elif 'privmsg' in data.lower() or (data[0] == ':' and data.find('@') > -1):
    #elif 'privmsg' in data.lower():
    #    # ex: data = ":r_!~r@ec2-18-188-176-66.us-east-2.compute.amazonaws.com PRIVMSG #test :t_msg"
    #    # ex: str_result = "[10/09/23 23:07:35.42] #test  <r_!~r>    test"
    #    usr = data[1:data.index('@'):1]
    #    msg = data[data.rfind(':')+1:-1:1]
    #    str_print = channel+'  <'+usr+'>    '+msg
    #    str_time = get_time_now()
    #    str_result = '['+str_time+'] '+str_print
    elif 'privmsg' in data.lower():
        # ex: data = ':Manga13!uid623229@id-623229.helmsley.irccloud.com PRIVMSG #atropa :@Cryptic420: I love teddy and love 2cc, I just think 2cc is underestimated by everyone 🧸\r\n'
        # ex: str_restul = '[10/11/23 09:19:15.32] #test  <n2_sales_force!~r>    @Cryptic420: I love teddy and love 2cc, I just think 2cc is underestimated by everyone 🧸'
        parts = data.split()
        usr_full = parts[0]
        usr_full = usr_full[1:] # remove preceeding ':'
        usr = usr_full[0:usr_full.index('@'):1]
        usr_loc = usr_full[usr_full.index('@'):len(usr_full)]
        
        msg_type = parts[1]
        ch_name = parts[2]
        
        msg = ' '.join(parts[3:len(parts)])
        msg = msg[1:] # remove preceeding ':'
        
        str_print = channel+'  <'+usr+'>    '+msg
        str_time = get_time_now()
        str_result = '['+str_time+'] '+str_print
        
    # handle default
    else:
        str_time = get_time_now()
        str_result = '['+str_time+'] '+data

    return str_result, str_time, usr, usr_full, usr_loc, msg, msg_type
    
def import_msg(server, port, nick='guest50040', channel='#test', data='nil_data', flag=-1):
    str_print = str_time = usr = usr_full = usr_loc = msg = msg_type = 'nil_str_import'
    # Print formatted msg to the console
    #str_print, str_time, usr, msg = parse_msg_string(data, channel)
    str_print, str_time, usr, usr_full, usr_loc, msg, msg_type = parse_msg_string(data, channel, flag)
    print(str_print)
    
    # update db
    keyVals = { 1:server, 2:port, 3:nick, 4:channel, 5:str_print, 6:str_time,
                7:usr_full, 8:usr_loc, 9:usr, 10:msg, 11:msg_type, 12:data }
    lst_db_return, success = db_add_log(keyVals)
    print(f'IMPORTED... {str_print}')
    
#------------------------------------------------------------#
#   DEFAULT SUPPORT                                          #
#------------------------------------------------------------#
READ_ME = f'''
    *DESCRIPTION*
        track IRC with domain, port, channel
        formats and prints user messges
        writes log to db
        
    *EXAMPLE EXECUTION*
        $ python3 {__filename} <usr|chan> <chan|usr>
        $ python3 {__filename} hlog #test
        $ python3 {__filename} #test hlog
        $ python3 {__filename} -h
        
    *NOTE* INPUT PARAMS...
        nil
'''
def wait_sleep(wait_sec : int, b_print=True): # sleep 'wait_sec'
    print(f'waiting... {wait_sec} sec')
    for s in range(wait_sec, 0, -1):
        if b_print: print('wait ', s, sep='', end='\n')
        time.sleep(1)
    print(f'waited... {wait_sec} sec')
        
def get_time_now(dt=True):
    if dt: return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[0:-4]
    return datetime.now().strftime("%H:%M:%S.%f")[0:-4]
    
def read_cli_args():
    print(f'\nread_cli_args...\n # of args: {len(sys.argv)}\n argv lst: {str(sys.argv)}')
    for idx, val in enumerate(sys.argv): print(f' argv[{idx}]: {val}')
    print('read_cli_args _ DONE\n')
    return sys.argv, len(sys.argv)

def run_tracker(usr_name='hlog', chan_name='#test', run_imports=False):
    if run_imports:
        # run w/ maria_irc_100823, maria_irc_100823_2, maria_irc_100923_2 -> dt format = '[4:37pm]'
        lines = maria_irc_100823.str_alt.split('\n')
        for line in lines: import_msg("irc.debian.org", 6667, 'hlog_import', '#atropa', line, flag=0)
        lines = maria_irc_100823_2.str_alt.split('\n')
        for line in lines: import_msg("irc.debian.org", 6667, 'hlog_import', '#atropa', line, flag=0)
        lines = maria_irc_100923_2.str_alt.split('\n')
        for line in lines: import_msg("irc.debian.org", 6667, 'hlog_import', '#atropa', line, flag=1)

        # run w/ maria_irc_101023_0, maria_irc_101023_1 -> dt format = '[4:37pm]'
        lines = maria_irc_101023_0.str_alt.split('\n')
        for line in lines: import_msg("irc.debian.org", 6667, 'hlog_import', '#atropa', line, flag=2)
        lines = maria_irc_101023_1.str_alt.split('\n')
        for line in lines: import_msg("irc.debian.org", 6667, 'hlog_import', '#atropa', line, flag=2)
        
        # run w/ maria_irc_100923, maria_irc_100923_tot -> dt format = 'Oct 08'
        lines = maria_irc_100923.str_alt.split('\n')
        for line in lines: import_msg("irc.debian.org", 6667, 'hlog_import', '#atropa', line)
        lines = maria_irc_100923_tot.str_alt.split('\n')
        for line in lines: import_msg("irc.debian.org", 6667, 'hlog_import', '#atropa', line)
        
    else:
        try:
            # run tracker
            track_msgs("irc.debian.org", 6667, usr_name, chan_name) # IRC server, port, nick, channel & channel pw (if required)
            
            # run tracker
            ch_lst = ["#test", "#pulsechain", "#atropa"]
            #track_msgs("irc.debian.org", 6667, 'hlog', ch_lst[2]) # IRC server, port, nick, channel & channel pw (if required)
            #track_msgs("irc.debian.org", 6667, 'hlog0', ch_lst[1]) # IRC server, port, nick, channel & channel pw (if required)
            
            # Create and start two threads
            #ping_thread = threading.Thread(target=send_ping_commands)
            #message_thread = threading.Thread(target=listen_for_messages)
            #ping_thread.start()
            #message_thread.start()
        except Exception as e:
            print(f'Error: {e}')
        
if __name__ == "__main__":
    ## start ##
    run_time_start = get_time_now()
    print(f'\n\nRUN_TIME_START: {run_time_start}\n'+READ_ME)
    lst_argv_OG, argv_cnt = read_cli_args()
    
    ## exe ##
    #run_tracker(run_imports=True)
    if '-h' in lst_argv_OG or '--help' in lst_argv_OG:
        print(READ_ME)
    elif len(lst_argv_OG) == 1:
        run_tracker(run_imports=False)
    else: # $ python3 track_irc.py <usr|chan> <chan|usr>
        usr_name = lst_argv_OG[1]
        ch_name = lst_argv_OG[2]
        if lst_argv_OG[1].startswith('#'):
            ch_name = lst_argv_OG[1]
            usr_name = lst_argv_OG[2]
        run_tracker(usr_name, ch_name, run_imports=False)
    
    ## end ##
    print(f'\n\nRUN_TIME_START: {run_time_start}\nRUN_TIME_END:   {get_time_now()}\n')

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')
