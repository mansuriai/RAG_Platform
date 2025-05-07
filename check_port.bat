# check_port.bat

@echo off
echo Checking if port 8601 is in use or accessible...

netstat -an | find ":8601" 

echo.
echo If you see any entries above, the port is being used by a process.
echo.

echo Testing port accessibility...
echo Attempting to connect to localhost:8601

powershell -Command "try { $client = New-Object System.Net.Sockets.TcpClient('localhost', 8601); if($client.Connected) { Write-Host 'Connection successful!' } else { Write-Host 'Connection failed.' } $client.Close() } catch { Write-Host 'Connection error: ' $_.Exception.Message }"

echo.
echo Now checking if any processes are blocking the port...
echo.

tasklist | findstr streamlit

echo.
echo Firewall status:
netsh advfirewall show currentprofile 

echo.
echo Press any key to exit...
pause > nul