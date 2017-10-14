def writeXML(records, filename, ownerName, ownerNumber):
#This is an XML version I added to make this compatible with the SMS Backup and Restore tools since 
#I was having problems creating databases and interacting with the SQLLite on my android.
    #in the version I downloaded, he was changing records with the ExplodeTextRecords, causing the need to re-run the entire program again. 
    #Instead, I created a copy of records (in this version its inside the function, but previous versions had it outside) mainly for testing. 
    
    fout = open(filename, "w");
    fout.write("<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>\n");
    fout.write('<?xml-stylesheet type="text/xsl" href="sms.xsl"?>\n');
    
    for i in records:
        if (str(type(i)).find("TextConversationList") != -1):
            for j in i:
                count += 1;
        
    fout.write('<smses count="' + str(count) + '">');
    
    for i in records:
#        print(count, isinstance(i,TextRecord), isinstance(i,TextConversationList), type(i))
#        This print statement was checking the types. I was having problems getting the if statement to correctly get the type/isinstance working
#        so instead I used a roundabout way. 

        if (str(type(i)).find("TextConversationList") != -1):
            for j in i:
#                print (j.contact.name, j.contact.phonenumber, j.receiver.phonenumber)
#                This print statement is a checker because I'm still getting some problems with both numbers being the "###ME###" number. 
#                In such a case, I think (for many instances) we can check a sandwich principle (if before and after are the same number we can conclude that the middle number is the same. 
#                Other cases I'm not so sure about. 
                if j.contact.name=="###ME###" or j.contact.name==ownerName or j.contact.phonenumber == ownerNumber or j.contact.phonenumber == "1" + ownerNumber:
                    texttype = 2;
                    number   = j.receiver.phonenumber
                    if not number:
                        print ("No number for %s" % (j.receiver.name))
                else:
                    texttype = 1;
                    number   = j.contact.phonenumber
                    if not number:
                        print ("No number for %s" % (j.contact.name))
                fout.write('<sms protocol="0" address="' + str(number) + '" date="' + getEpoch(str(j.date.strftime("%Y-%m-%d %H:%M:%S"))) + '000" type="' + str(texttype) + '" subject="null" body="' + j.text.replace("\n", " ").replace("\r", " ").replace("&", " and ").replace("<", "").replace(">", "").replace("\"", "'") + '" toa="0" sc_toa="0" service_center="null" read="1" status="-1" locked="0" date_sent="' + getEpoch(str(j.date.strftime("%Y-%m-%d %H:%M:%S"))) + '000" readable_date="' + str(j.date) + '" contact_name="(Unknown)" />\n');
            count += 1;    
    fout.write('</smses>\n');
    fout.close();

def getEpoch(time):
    utc_time = datetime.datetime.strptime(str(time), "%Y-%m-%d %H:%M:%S")
    epoch_time = (utc_time - datetime.datetime(1970, 1, 1)).total_seconds()
    return str(math.floor(epoch_time))
