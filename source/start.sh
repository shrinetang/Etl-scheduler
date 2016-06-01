#!/bin/bash - 
#===============================================================================
#
#          FILE: start.sh
# 
#         USAGE: sh start.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: caodaijun
#  ORGANIZATION: 
#       CREATED: 04/10/14 18:46:07 CST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

function main {
	cd $(dirname "$0")

	if [ -f "var/supervisord.pid" ]; then
		kill $(cat "var/supervisord.pid") &> /dev/null
		if [ $? -ne 0 ]; then
			echo "supervisor is running, and can not kill!"
			return
		fi

		sleep 1
		if [ -f "var/supervisord.pid" ]; then
			echo "supervisor is running, pid file is exist!"
			return
		fi
	fi

	supervisord -c etc/supervisor.conf
}


main $*
