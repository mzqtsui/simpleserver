
#!/usr/bin/bash

#------------------------------#
# Format of command            #
#------------------------------#
# python client.py -i <Server IP> -p <UDP port> -c <get | put> -l <localfile> -r <remotefile>
# 
# to use localhost, leave -i empty with ""

#------------------------------#
# Sample get                   #
#------------------------------#
# python client.py -i "" -p 62618 -c get -l test_local -r test_remote


#------------------------------#
# Sample put                   #
#------------------------------#
# python client.py -i 129.97.167.133 -p 53688 -c put -l test_local -r test_remote
