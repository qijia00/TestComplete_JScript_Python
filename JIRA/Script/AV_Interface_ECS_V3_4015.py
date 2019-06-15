#JIRA ECS_V3-4015: Verify AV interface integration with WinECU
#------------------------------------------------------------
#function name :  ECS_V3_4015(hostIP)
#Parameters    :  hostIP for V3.6 ECU (if you want to test V3.5, then use the SSU IP)
#Description   :  Send command with different line breaks, either OK or ERROR should be received.
#------------------------------------------------------------

def ECS_V3_4015(hostIP):
  
    import socket
  
    #import data from excel with multiple sheets
    path = Project.Path + 'Data\\ECS_V3_4015.xlsx'
    excel = Sys.OleObject['Excel.Application'].Workbooks.Open(path)
    sheetHost = excel.Sheets.Item['Host']
    sheetCommand = excel.Sheets.Item['Command']
    sheetCRLF = excel.Sheets.Item['CRLF'] 
  
    #import data from sheetHost for Host ip and port
    #hostIP = VarToString(sheetHost.Cells.Item[1, 2]) #if the value comes from excel
    port = VarToInt(sheetHost.Cells.Item[2, 2])

    #create a communication chanel between TestComplete to Host via socket s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try:
        s.connect((hostIP, port))
    except:
        Log.Error('unable to connect')
        return
    Log.Message('connected to HOST %s via PORT %d'  %(hostIP, port))
    
    #response = str(s.recv(4096)) #returns b'ECS AV Interface\r\n\r\n'
    response = str(s.recv(4096), 'UTF-8').strip() #use 'UTF-8' to get rid of b, use strip to get rid of \r\n\r\n    
    #read connect prompt "ECS AV Interface"
    if response == 'ECS AV Interface':
        Log.Message(response)
    elif response:
        Log.Error(response)
    else:
        Log.Error('failed to get response')
        return

    #form command from excel sheets
    RowCount = sheetCommand.UsedRange.Rows.Count
    ColumnCount = sheetCommand.UsedRange.Columns.Count
    for x in range(2, RowCount+1):
        command = VarToString(sheetCommand.Cells.Item[x, 1]) + ' ' + VarToString(sheetCommand.Cells.Item[x, 2]) \
        + ' ' + VarToString(sheetCommand.Cells.Item[x, 3]) 
            
        for y in range(1, 5):
            lineBreak = str(sheetCRLF.Cells.Item[y, 1])
            fCommand = command + lineBreak
            Log.Message(fCommand) #you thought fCommand is ':RS 0066FF23 2\r', where \r is invisible as line break
            #actualy fCommand is ':RS 0066FF23 2\\r', where \\ means \, so \r is visible as part of the string          
            #use decode('unicode_escape') to make \r invisible, then
            decodedfCommand = bytes(fCommand, 'UTF-8').decode('unicode_escape')
            #convert command from string decodedfCommand ':RS 0066FF23 2\r' to bytes then send            
            s.send(bytes(decodedfCommand, 'UTF-8'))
            
            try:
                response = str(s.recv(4096), 'UTF-8').strip()
            except socket.timeout:    
                Log.Error('failed to get response')
            else:
                if response == ':OK':
                    Log.Message(response)
                elif response:
                    Log.Message(response)
                      
    excel.close
    
#for quick test
def test():
    ECS_V3_4015("10.215.21.133")