import socket
import sys
import time
import zipfile
import re
import os


regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
			25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
			25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
			25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''

if __name__ == "__main__":
	server_path = str(os.path.dirname(os.path.realpath(__file__)))
	host_name = socket.gethostname()
	host_ip = socket.gethostbyname(host_name)
	if len(sys.argv) > 1:
		if sys.argv[1] == "--help":
			print("Usage: python3 file-server.py [options]...")
			print("Options:")
			print("  --help\t\t Display this information")
			print("  --address [ip]\t Define the ip server address (optionally if the ip is not getting detected automatically)")
			sys.exit()
		elif sys.argv[1] == "--address":
			try:
				server_address = str(sys.argv[2])
			except IndexError:
				print("The given ip address was invalid")
				sys.exit("Please use --help if you need assistance")

			if re.search(regex, server_address) is None:
				sys.exit("{} is an invalid ip address".format(server_address))

			host_ip = server_address
		else:
			print("The given option was invalid")
			sys.exit("Please use --help if you need assistance")

	print("Server directory: {}".format(server_path))
	print("Server ip address: {}".format(host_ip))
	s = socket.socket()
	s.bind((host_ip,9999))
	s.listen(3)

	while True:
		sc, address = s.accept()

		print("Connected client {}".format(address))
		filename = sc.recv(1024)
		filename = filename.decode("utf-8")
		try:
			f = open(filename, "wb")
			print("Receiving file {}...".format(filename))
			start = time.time()
			l = sc.recv(1024)
			while l:
				f.write(l)
				l = sc.recv(1024)

			print("File {} received! Time elapsed {} seconds.".format(filename, time.time() - start))
			f.close()
			if ".zip" in filename:
				print("Extracting {}...".format(filename))
				zip_file = zipfile.ZipFile(server_path + "/" + filename, 'r')
				zip_file.extractall(server_path + "/")
				zip_file.close()
				print("{} extracted".format(filename))
		except:
			print("Error receiving {}".format(filename))

	sc.close()
