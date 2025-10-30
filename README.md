# webticket

This python tool is designed to check HTTP/HTTPS on ports 80, 8080 and 443 from a given IP/Hostname.

Checking websites manually with curl, burp or browser can take some time or you may forget to check all ports.

The goal is to automate it to save time and prevent skipping an existing website.

### Usage

Run the script with python3.

You input a known IP address or hostname and the program sends a request 
for HTTP/HTTPS (you can specify one or both) common ports and send back only 2xx[OK] or 3xx[Forbidden] responses.

After checking, it runs 'whatweb' _(external tool)_ for every affirmative site. 

If HTTPS site exists, it checks for ssl certificate with 'openssl' _(external tool)_ and retreive it.

All this info will be printed in your console as a web "ticket" for every valid request.

Important: If you are not on a Linux pentesting distro like Kali, Parrot,... 
you may need to install 'whatweb' and 'openssl' with your distro's packet manager to obtain full functionality of the script.

_______________________

Feel free to add more ports by editing line 8.

_______________________

_______________________

###### Tool created by Exbinary


