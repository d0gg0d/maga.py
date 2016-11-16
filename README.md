# maga.py
Validates a list of emails using an SMTP server that allows email validity tests.

HOW TO USE:
	Required Flags:
		-a	-	Telnet Address
		-i	-	File that contains emails
		-f	-	Your email address
	The following are optional flags if you need it:
		-o	-	File output name
		-p	-	Port number in case their SMTP port is not port 25
		--log=LEVEL -	"Level" can be DEBUG, INFO, WARNING, ERROR, CRITICAL
					Default is INFO. The other levels 
					are unused with the exception of 
					the DEBUG level. There are a couple 
					of lines that use the DEBUG level, 
					but not many.
				Currently a log is created for diagnostic purposes.
				Should the program act up, one should check the log
				to see if there are any anomalies or errors.

CURRENT ISSUES:
	- If you get too many invalid emails, the SMTP server will kick you. The
		program will think that it's the end and stop the test.
	- SMTP servers that give non-standard error codes will make the program
		function strangely if there's an error.
	- Trump is president.
