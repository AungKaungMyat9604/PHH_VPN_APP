-- AppleScript to launch PHH VPN Client (double-clickable app)
-- This creates a double-clickable app on macOS

on run
    set scriptPath to POSIX path of (path to me)
    set scriptDir to do shell script "dirname " & quoted form of scriptPath
    set commandPath to scriptDir & "/PHH_VPN_Client.command"
    
    try
        do shell script "cd " & quoted form of scriptDir & " && " & quoted form of commandPath
    on error errMsg
        display dialog "Error launching PHH VPN Client: " & errMsg buttons {"OK"} default button 1
    end try
end run
