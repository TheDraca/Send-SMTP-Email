import smtplib, ssl, json

#Set what our settings file is called
SettingsFile = "SMTPSettings.json"

#Read the file each time an item is used
def GetSetting(Setting, SettingName):
    with open(SettingsFile) as JSONFile:
        SettingsJSON = json.load(JSONFile)
    return SettingsJSON[Setting][SettingName]

#Build Message with correct headers before hand
def MessageBuild(To,Message,From=GetSetting("Mail","From"),Subject=GetSetting("Mail","Subject")):
    return "From: {0}\r\nTo: {1}\r\nSubject: {2}\r\n\r\n{3}".format(From,To,Subject,Message)

#Create a username raw string that can included the escapeing character \
def LoginUsernameBuild(LoginDomain=GetSetting("Exchange","LoginDomain"),LoginUsername=GetSetting("Exchange","LoginUsername")):
    return (r"{0}\{1}".format(LoginDomain,LoginUsername))


def SendEmail(Message=GetSetting("Mail","MessageBody")):
    try:
        #Connect to set server
        server = smtplib.SMTP(GetSetting("Exchange","Host"),GetSetting("Exchange","Port"))

        # Start a secure connection with a new SSL context
        server.starttls(context=ssl.create_default_context()) 

        #Login to exchaange with out set username and password, prompt for password if not given
        if GetSetting("Exchange","LoginPassword") == "":
            Password = input("Password: ")
            server.login(LoginUsernameBuild(), Password)
        else:
            server.login(LoginUsernameBuild(), GetSetting("Exchange","LoginPassword"))

        #Finally sent out the email
        for Recipient in GetSetting("Mail","To"):
            server.sendmail(GetSetting("Mail","From"),Recipient,MessageBuild(Recipient,Message))
            print("Mail Sent")
    except:
        print("Error sending message")
