__filename = 'db_controller.py'
__fname = 'db_controller'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

import sites_env #required: sites_env/__init__.py
from tools import *

'''
# https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
# https://docs.sqlalchemy.org/en/13/dialects/mysql.html#module-sqlalchemy.dialects.mysql.pymysql
    mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
# https://pymysql.readthedocs.io/en/latest/user/examples.html
    #NOTE: '$ pip3' == '$ python3.6 -m pip'
        $ python3 -m pip install PyMySQL
        $ python3.7 -m pip install PyMySQL
    '''
import pymysql.cursors

logenter(__filename, " IMPORTs complete:- STARTING -> file '{__filename}' . . . ", simpleprint=True, tprint=True)

dbHost = sites_env.dbHost #read_env()
dbName = sites_env.dbName #read_env()
dbUser = sites_env.dbUser #read_env()
dbPw = sites_env.dbPw     #read_env()

db = None
cur = None

strErrCursor = "global var cur == None, returning -1"
strErrConn = "FAILED to connect to db"

#====================================================#
##              db connection support               ##
#====================================================#
def open_database_connection():
    funcname = f'({__filename}) open_database_connection'
    logenter(funcname, simpleprint=False, tprint=False)

    # Connect to DB #
    try:
        global db, cur

        # legacy manual db connection #
        db = pymysql.connect(host=dbHost,
                             user=dbUser,
                             password=dbPw,
                             db=dbName,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor()

        if cur == None:
            logerror(funcname, "database cursor received (cur) == None; returning None", "FAILED to connect to db", simpleprint=False)
            return -1

        loginfo(funcname, f' >> CONNECTED >> to db {dbName} successfully!', simpleprint=True)
    except Exception as e:
        logerror(funcname, "exception hit", "FAILED to connect to db", simpleprint=False)
        printException(e, debugLvl=2)
        return -1
    finally:
        return 0

def close_database_connection():
    funcname = f'({__filename}) close_database_connection'
    logenter(funcname, simpleprint=False, tprint=False)

    global db, cur
    if db == None:
        logerror(funcname, "global var db == None; returning", "FAILED to close db connection", simpleprint=False)
        return

    db.commit()
    db.close()

    db = None
    cur = None
    loginfo(funcname, ' >> CLOSED >> db successfully!', simpleprint=True)

def exeStoredProcedure(argsTup, strProc, strOutParam=None, exe_select=False):
    funcname = f'({__filename}) exeStoredProcedure({argsTup}, {strProc}, {strOutParam}, exe_select={exe_select})'
    logenter(funcname, simpleprint=False, tprint=True)

    #============ open db connection ===============#
    global cur
    if open_database_connection() < 0:
        return -1

    if cur == None:
        logerror(funcname, strErrCursor, strErrConn, simpleprint=False)
        return -1

    #============ perform db query ===============#
    procArgs = 'nil'
    rowCnt = 'nil'
    rows = 'nil'

    try:
        if exe_select:
            procArgs = argsTup
            rowCnt = cur.execute(strProc)
            rows = cur.fetchall()
        else:
            procArgs = cur.callproc(f'{strProc}', argsTup)
            rowCnt = cur.execute(f"select {strOutParam};") if strOutParam != None else -1
            rows = cur.fetchall()

        loginfo(funcname, f" >> RESULT 'call {strProc}' procArgs: {procArgs};", simpleprint=True)
        loginfo(funcname, f" >> RESULT 'call {strProc}' rowCnt: {rowCnt};", simpleprint=True)
        #loginfo(funcname, f' >> Printing... rows', *rows, simpleprint=True)
        getPrintListStr(lst=rows, strListTitle='  >> Printing... rows', useEnumerate=True, goIdxPrint=True, goPrint=True)
        #loginfo(funcname, f' >> Printing... rows[0]:', rows[0], simpleprint=True)
        
        result = None
        if strOutParam == None: # stored proc invoked w/o OUT param
            result = rows
        else: # stored proc invoked w/ OUT param
            result = rows[0][strOutParam]
            if isTypeInteger(rows[0][strOutParam]):
                result = int(rows[0][strOutParam])
    except Exception as e: # ref: https://docs.python.org/2/tutorial/errors.html
        #============ handle db exceptions ===============#
        strE_0 = f"Exception hit... \nFAILED to call '{funcname}'; \n\nprocArgs: {procArgs}; \n\nreturning -1"
        strE_1 = f"\n __Exception__: \n{e}\n __Exception__"
        logerror(funcname, strE_0, strE_1, simpleprint=False)
        result = -1
    finally:
        #============ close db connection ===============#
        close_database_connection()
        return result
        
def exe_stored_proc(iUserID=-1, strProc='', dictKeyVals={}):
    funcname = f'({__filename}) exe_stored_proc(iUserID={iUserID}, strProc={strProc}, dictKeyVals={dictKeyVals})'
    logenter(funcname, simpleprint=False, tprint=True)

    argsTup = () # generate tuple of vals from dictKeyVals (dict order maintained in python3.7+)
    argsTup = [argsTup + (dictKeyVals[k],) for k in dictKeyVals]
    strOutParam = None
    return exeStoredProcedure(argsTup, strProc, strOutParam)
    
def exe_select_stat(iUserID=-1, strSel='', dictKeyVals={}):
    funcname = f'({__filename}) exe_select_stat(iUserID={iUserID}, strProc={strProc}, dictKeyVals={dictKeyVals})'
    logenter(funcname, simpleprint=False, tprint=True)
    
    argsTup = () # generate tuple of vals from dictKeyVals (dict order maintained in python3.7+)
    argsTup = [argsTup + (dictKeyVals[k],) for k in dictKeyVals]
    strOutParam = None
    return exeStoredProcedure(argsTup, strSel, strOutParam, exe_select=True)

def sel_2_tbl_query(d_col_val_where_1={},
                        d_col_val_where_2={},
                        lst_col_sel_1=[],
                        lst_col_sel_2=[],
                        str_tbl_1='',
                        str_tbl_2='',
                        str_tbl_as_1='',
                        str_tbl_as_2='',
                        bGetAll=False):
    funcname = f'({__filename}) sel_2_tbl_query(d_col_val_where_1={d_col_val_where_1}, d_col_val_where_2={d_col_val_where_2}, lst_col_sel_1={lst_col_sel_1}, lst_col_sel_2={lst_col_sel_2}, str_tbl_as_1={str_tbl_as_1}, str_tbl_as_2={str_tbl_as_2}, bGetAll={bGetAll})'
    logenter(funcname, simpleprint=False, tprint=True)

    # generate string using lst_col_sel_1|2:
    #   EX: 'SELECT <columns> FROM candidates cand INNER JOIN candidate_apps capp'
    strSel = ''
    loginfo(funcname, f'strSel: {strSel}', simpleprint=True)
    if bGetAll:
        #logalert(funcname, f"bGetAll: {bGetAll}", simpleprint=False)
        strSel = f'SELECT {str_tbl_as_1}.*, {str_tbl_as_2}.*, {str_tbl_as_1}.id AS {str_tbl_as_1}_id, {str_tbl_as_2}.id AS {str_tbl_as_2}_id FROM {str_tbl_1} {str_tbl_as_1} INNER JOIN {str_tbl_2} {str_tbl_as_2} ON {str_tbl_as_2}.fk_{str_tbl_as_1}_id = {str_tbl_as_1}.id'
    else:
        # init query string w/ select clause
        strSel = f"SELECT {str_tbl_as_1}.id AS {str_tbl_as_1}_id, {str_tbl_as_2}.id AS {str_tbl_as_2}_id,"
        
        # generate & append str_tbl_as_1 select clause
        #   loop through 'lst_col_sel_1' (client side str_tbl_as_1 col names selected)
        for idx, col in enumerate(lst_col_sel_1):
            c = col.lower()
            if idx < len(lst_col_sel_1) - 1 or len(lst_col_sel_2) > 0:
                strSel = f"{strSel} {str_tbl_as_1}.`{c}`,"
            else:
                strSel = f"{strSel} {str_tbl_as_1}.`{c}`"

        # generate & append str_tbl_as_2 select clause
        #   loop through 'lst_col_sel_2' (client side str_tbl_as_2 col names selected)
        for idx, col in enumerate(lst_col_sel_2):
            c = col.lower()
            if idx < len(lst_col_sel_2) - 1:
                strSel = f"{strSel} {str_tbl_as_2}.`{c}`,"
            else:
                strSel = f"{strSel} {str_tbl_as_2}.`{c}`"
                
        # append FROM clause
        strSel = f"{strSel} FROM {str_tbl_1} {str_tbl_as_1} JOIN {str_tbl_2} {str_tbl_as_2} ON {str_tbl_as_2}.fk_{str_tbl_as_1}_id = {str_tbl_as_1}.id"

    # print current strSel
    loginfo(funcname, f'strSel: {strSel}', simpleprint=True)
    
    # check / init WHERE clause
    logalert(funcname, f"d_col_val_where_1: {d_col_val_where_1}\n", f"d_col_val_where_2: {d_col_val_where_2}", simpleprint=False)
    if len(d_col_val_where_1) > 0 or len(d_col_val_where_2) > 0:
        strSel = f"{strSel} WHERE"

        # generate string using d_col_val_where_1|2:
        #   'WHERE <col=val>'
        for idx, key in enumerate(d_col_val_where_1):
            k = key.lower()
            if idx < len(d_col_val_where_1) - 1 or len(d_col_val_where_2) > 0: # check appending 'and' as needed
                if k[0:3:1] == 'dt_': # check for handling datetime inputs & cols
                    strSel = f"{strSel} DATE({str_tbl_as_1}.{k}) = DATE('{d_col_val_where_1[key]}') and"
                else:
                    strSel = f"{strSel} {str_tbl_as_1}.{k} = '{d_col_val_where_1[key]}' and"
            else:
                if k[0:3:1] == 'dt_':
                    strSel = f"{strSel} DATE({str_tbl_as_1}.{k}) = DATE('{d_col_val_where_1[key]}')"
                else:
                    strSel = f"{strSel} {str_tbl_as_1}.{k} = '{d_col_val_where_1[key]}'"
        for idx, key in enumerate(d_col_val_where_2):
            k = key.lower()
            if idx < len(d_col_val_where_2) - 1: # check appending 'and' as needed
                if k[0:3:1] == 'dt_': # check for handling datetime inputs & cols
                    strSel = f"{strSel} DATE({str_tbl_as_2}.{k}) = DATE('{d_col_val_where_2[key]}') and"
                else:
                    strSel = f"{strSel} {str_tbl_as_2}.{k} = '{d_col_val_where_2[key]}' and"
            else:
                if k[0:3:1] == 'dt_':
                    strSel = f"{strSel} DATE({str_tbl_as_2}.{k}) = DATE('{d_col_val_where_2[key]}')"
                else:
                    strSel = f"{strSel} {str_tbl_as_2}.{k} = '{d_col_val_where_2[key]}'"
                
    # print current strSel
    loginfo(funcname, f'strSel: {strSel}', simpleprint=True)
    
    # append end query sorting
    strSel = f"{strSel} ORDER BY {str_tbl_as_2}_id DESC;"
    
    # print current strSel
    loginfo(funcname, f'strSel: {strSel}', simpleprint=True)
    
    argsTup = (d_col_val_where_1, d_col_val_where_2, lst_col_sel_1, lst_col_sel_2, bGetAll)
    strProc = strSel
    strOutParam = None
    return exeStoredProcedure(argsTup, strProc, strOutParam, exe_select=True)

#===========================================================#
# db_controller support (migrated from gms_post)
#===========================================================#
def procValidatePIN(strPIN='-1'):
    funcname = f'({__filename}) procValidatePIN(strPIN={strPIN})'
    logenter(funcname, simpleprint=False, tprint=True)

    argsTup = (strPIN, 'p_Result')
    strProc = 'ValidatePIN'
    strOutParam = '@_ValidatePIN_1'
    return exeStoredProcedure(argsTup, strProc, strOutParam)

def procGetEmpData(strPIN=''):
    funcname = f'({__filename}) procGetEmpData({strPIN})'
    logenter(funcname, simpleprint=False, tprint=True)

    argsTup = (strPIN,)
    strProc = 'GetEmpDataFrom_PIN'
    strOutParam = None
    return exeStoredProcedure(argsTup, strProc, strOutParam)
    
    #exeStoredProcedure(argsTup, strProc, strOutParam=None, exe_select=False)
    
def isTypeInteger(varCheck=None):
    if varCheck == None:
        return False
    return isinstance(varCheck, int)
    
#====================================================#
#====================================================#

loginfo(__filename, f"\n CLASSES & FUNCTIONS initialized:- STARTING -> additional '{__filename}' run scripts (if applicable) . . .", simpleprint=True)
loginfo(__filename, f"\n  DONE Executing additional '{__filename}' run scripts ...", simpleprint=False)
print('#======================================================================#')
