#Set variables

domain_home = raw_input('Enter WLS Domain Path: ')

# Set the path to the domain configuration file
config_file = domain_home + '/config/config.xml'

#Load the Domain Configuration
readDomain(domain_home)

schema_pwd = raw_input('Enter the new password in plain text format: ')
schema_prfx = raw_input('Enter RCU Schema prefix: ')
user_input = raw_input('Do you want to replace ATP DB Connection Url (yes/no): ')
db_conn_url = raw_input('Enter the ATP DB connection url: ')


jdbc_ds_list = ls('/JDBCSystemResource/')

jdbc_ds_list = [line.strip() for line in jdbc_ds_list.split('\n') if line.strip()]
jdbc_ds_list = [ds.replace('drw-   ', '') for ds in jdbc_ds_list]

# Create an empty list to store the datasource names related to RCU
RCU_DataSources = []

# Loop through each datasource and check if the username starts with provided RCU prefix
for ds in jdbc_ds_list:
    cd('/JDBCSystemResource/' + ds + '/JdbcResource/' + ds + '/JDBCDriverParams/NO_NAME_0/Properties/NO_NAME_0/Property/user')
    if get('Value').startswith(schema_prfx):
       RCU_DataSources.append(ds)
if len(RCU_DataSources) !=0:
   for ds in RCU_DataSources:
      print('--------Updating password for '+ ds +'--------')
      cd('/JDBCSystemResource/' + ds + '/JdbcResource/' + ds + '/JDBCDriverParams/NO_NAME_0')
      set('PasswordEncrypted', encrypt(schema_pwd))
      print('--------New Password updated successfully for ' + ds +'--------')
      if user_input.lower() == "yes":
        print('--------Updating connection pool url for '+ ds +'--------')
        cd('/JDBCSystemResource/' + ds + '/JdbcResource/' + ds + '/JDBCDriverParams/NO_NAME_0')
        set('URL',db_conn_url)
        print('--------Connection pool url updated successfully for '+ ds + '--------')
      else:
        print('--------Updation of connection pool url is not required for '+ ds + 'as per input provided--------') 
   print("\n")
   print("------------------------------------------------------------------------------")    
   updateDomain()
else:
   print("Please Check the RCU schema prefix again, looks like it is incorrect")

closeDomain()

#Updating the jps-config-jse.xml which will update the cwallet.sso file with new password
print("\n")
print("updating jps-config-jse.xml with new password\n")
modifyBootStrapCredential(jpsConfigFile=domain_home + '/config/fmwconfig/jps-config-jse.xml',username=schema_prfx + '_OPSS',password=schema_pwd)
exit()
