#!/bin/bash

CONNECTION_STRING=$1  
DOMAIN_HOME=$2


display_usage() { 
	echo "This script must be run with oracle user." 
	echo -e "\nUsage: $0 <JDBC_CONN_URL> <DOMAIN_HOME> \n" 
	} 
# if less than two arguments supplied, display usage 
	if [  $# -le 1 ] 
	then 
		display_usage
		exit 1
	fi 
 
# check whether user had supplied -h or --help . If yes display usage 
	if [[ ( $@ == "--help") ||  $@ == "-h" ]] 
	then 
		display_usage
		exit 0
	fi 
 
# display usage if the script is not run as oracle user 
echo "You are logged in as `whoami`";

        if [ `whoami` != "oracle" ]; then
         echo "Must be logged on as oracle to run this script."
         exit 1
        fi 

# Checking if the jps config files exist in provided domain home
if [ -f "$DOMAIN_HOME/config/fmwconfig/jps-config.xml" ]  && [ -f "$DOMAIN_HOME/config/fmwconfig/jps-config-jse.xml" ]; then
 echo "Changing the JDBC url from JPS Configuration files"

# Updated jdbc url from jps config files
 awk -v con="$CONNECTION_STRING" '{gsub(/value="jdbc:oracle:thin.*"/, "value=\""con"\"")}1' $DOMAIN_HOME/config/fmwconfig/jps-config.xml > /tmp/jps-config.xml && mv /tmp/jps-config.xml $DOMAIN_HOME/config/fmwconfig/jps-config.xml

 awk -v con="$CONNECTION_STRING" '{gsub(/value="jdbc:oracle:thin.*"/, "value=\""con"\"")}1' $DOMAIN_HOME/config/fmwconfig/jps-config-jse.xml > /tmp/jps-config-jse.xml && mv /tmp/jps-config-jse.xml $DOMAIN_HOME/config/fmwconfig/jps-config-jse.xml

 echo "JPS configuration file changes successfully with the new JDBC urls"
else
 echo "You have entered wrong DOMAIN_HOME, Please check again"
fi
