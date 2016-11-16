#!/usr/bin/python
import telnetlib
import time
import argparse
import logging

def fileOpen(filename, address, fromAddr, output, port):
	try: # Opens email input file. Checks if file exists or if file is empty.
		infile = open( filename, 'r' )
		if output != None:
			outfile = open(output, 'w')
		for INemail in infile:
			if INemail == None:
				raise SystemExit
			else:
				email = cleanInput( INemail )
				answer = run_check( email, address, fromAddr, port )
				if output != None:
					outfile.write(answer)
					continue
	except:
		# print('Unexpected Error:', sys.exc_info()[0])
		raise SystemExit


def cleanInput(email): # Cleans email for extraneous characters
	email = email.strip('\n').strip('\t').strip('\r')
	return email

def exitTelnet(tnet): # Tears down connection to check next email
	tnet.close()
	logging.info( 'Connection closed...' )

def cleanClose(tnet): # Tears down connection and cleanly exits program
	tnet.close()
	logging.info( 'Connection closed...' )
	logging.info( 'Closing files & program...')
	infile.close()
	logging.info( 'Closing Input File...' )
	outfile.close()
	logging.info( 'Closing Output File...' )
	logging.info( 'Finished...' )
	raise SystemExit

def run_check(email, address, fromAddr, port):
	from_name, from_domain = fromAddr.split( '@' )
	helo = "helo {}".format( from_domain )
	sender = "mail from: <{}>".format( fromAddr )
	receiver = "rcpt to: <{}>".format( email )


	try: # telnet (client SMTP) 25
		logging.info( 'Telnetting in...' )
		TNET = telnetlib.Telnet( host=address, port=port, timeout=3 )
		response = TNET.read_until( b"\r\n" ).decode( encoding="utf-8" )
		logging.info( 'CONNECTED' )
		logging.info( response )
		if "421" in response:
			print('Service not available.')
			cleanClose(TNET)
		if "450" in response:
			print('Connecting too quickly.')
			cleanClose(TNET)
	except:
		logging.info('Connect failed\nExiting...')
		cleanClose(TNET)

	try: # helo (your SMTP address)
		logging.info( 'helo {}'.format( from_domain ) )
		TNET.write( helo.encode('ascii' )+ b"\r\n" )
		logging.info( 'helo!' )
		response = TNET.read_until( b"\r\n" ).decode( encoding="utf-8" )
		logging.info ( response )
	except:
		print('Unexpected Error:', sys.exc_info()[0])
		logging.debug( 'helo failed\nExiting...' )
		cleanClose( TNET )

	try: # mail from: <email@yourSMTPdomain>
		logging.info( 'mail from: {}...'.format( fromAddr ) )
		TNET.write( sender.encode( 'ascii' )+ b"\r\n" )
		logging.info( 'sender sent!' )
		response = TNET.read_until( b"\r\n" ).decode(encoding="utf-8" )
		logging.info( response )
	except:
		logging.debug( 'mail from location invalid\nExiting...')
		cleanClose( TNET )

	try: # rcpt to: <email@clientSMTPdomain>
		logging.info( 'rcpt to: <{}>....'.format(receiver) )
		TNET.write( receiver.encode('ascii') + b"\r\n" )
		logging.info('receiver set!')
		response = TNET.read_until( b"\r\n" ).decode(encoding="utf-8" )
		if "250" in response:
			print( '\033[92m'+'[+]'+'\033[0m'+'{}'.format( email ) )
			answer = '[+] {}\n'.format( email )
		elif "554" in response:
			print( '\033[91m'+'[-]'+'\033[0m'+'{}'.format( email ) )
			answer = '[+] {}\n'.format( email )
		else:
			print( '\033[91m'+'[-]'+'\033[0m'+'{}'.format( email ) )
			answer = '[-] {}\n'.format( email )
		logging.info( response )
	except:
		logging.debug( 'mail to location invalid\nExiting...')
		cleanClose( TNET )

	# Check for given email complete.
	# Tears down telnet connection and sleeps before check next email
	logging.info( 'Valid Check done.' )
	exitTelnet(TNET)
	time.sleep(.75)
	return answer

if __name__ == "__main__":
	logging.basicConfig(filename='maga.log',level=logging.INFO)

	parser = argparse.ArgumentParser( "Test for email validity.")
	parser.add_argument( "-a", "--address", required=True, help="Telnet address of client." )
	parser.add_argument( "-i", "--input", required=True, help="List of emails to be tested." )
	parser.add_argument( "-f", "--fromaddr", required=True, help="Mail from address (Your email address)." )
	parser.add_argument( "-o", "--output", required=False, help="File to write output to." )
	parser.add_argument( "-p", "--port", required=False, help="Port number for client's SMTP server." )

	args = vars( parser.parse_args() )

	address = args["address"] if args["address"] else None
	infile = args["input"] if args["input"] else None
	fromAddr = args["fromaddr"] if args["fromaddr"] else None
	output = args["output"] if args["output"] else None
	port = args["port"] if args["port"] else "25" 



	fileOpen(infile, address, fromAddr, output, port)