import socket
import sys
import os
import re
import time
import zipfile


regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
			25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
			25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
			25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''


def retrieve_file_paths(dirName):
	filePaths = []

	for root, directories, files in os.walk(dirName):
		for filename in files:
			filePath = os.path.join(root, filename)
			filePaths.append(filePath)

	return filePaths


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Use --help to print the argument list")
		sys.exit("No arguments were given")

	selected_option = str(sys.argv[1])
	if selected_option == "--help":
		print("Usage: python3 file-client.py [options]...")
		print("Options:")
		print("  --help\t\t Display this information")
		print("  --mode [mode]\t\t Define the mode that you want to use")
		print("               \t\t Available modes:")
		print("               \t\t   ?? single for single file transfer")
		print("               \t\t   ?? multi to transfer every file in the given path")
		print("               \t\t   ?? zip to compress the folder before sending it")
		print("  --dir  [path]\t\t Define the path of the file you want to share")
		print("  --file [filename]\t Define the name of the file you want to share")
		print("  --address [ip]   \t Define the ip address of the server")
		sys.exit()
	elif selected_option == "--mode":
		try:
			selected_mode = str(sys.argv[2]).lower()
		except IndexError:
			print("You need to define the mode you want to use")
			sys.exit("Please use --help if you need assistance")
	else:
		print("The given argument was invalid")
		sys.exit("Please use --help if you need assistance")

	if selected_mode == "single":
		try:
			first_string = str(sys.argv[3]).lower()
			if first_string == "--dir":
				try:
					filepath = str(sys.argv[4])
				except IndexError:
					print("The given path was invalid")
					sys.exit("Please use --help if you need assistance")
			elif first_string == "--file":
				try:
					filename = str(sys.argv[4])
				except IndexError:
					print("The given name of the file was invalid")
					sys.exit("Please use --help if you need assistance")
			elif first_string == "--address":
				try:
					server_address = str(sys.argv[4])
				except IndexError:
					print("The given ip address was invalid")
					sys.exit("Please use --help if you need assistance")
			else:
				print("The given option was invalid")
				sys.exit("Please use --help if you need assistance")

			second_string = str(sys.argv[5]).lower()
			if first_string == second_string == "--dir":
				print("The directory of the file was already given")
				sys.exit("Please use --help if you need assistance")
			elif first_string == second_string == "--file":
				print("The name of the file was already given")
				sys.exit("Please use --help if you need assistance")
			elif first_string == second_string == "--address":
				print("The ip address of the server was already given")
				sys.exit("Please use --help if you need assistance")
			if second_string == "--dir":
				try:
					filepath = str(sys.argv[6])
				except IndexError:
					print("The given path was invalid")
					sys.exit("Please use --help if you need assistance")
			elif second_string == "--file":
				try:
					filename = str(sys.argv[6])
				except IndexError:
					print("The given name of the file was invalid")
					sys.exit("Please use --help if you need assistance")
			elif second_string == "--address":
				try:
					server_address = str(sys.argv[6])
				except IndexError:
					print("The given ip address was invalid")
					sys.exit("Please use --help if you need assistance")

			third_string = str(sys.argv[7]).lower()
			if first_string == third_string == "--dir":
				print("The directory of the file was already given")
				sys.exit("Please use --help if you need assistance")
			elif first_string == third_string == "--file":
				print("The name of the file was already given")
				sys.exit("Please use --help if you need assistance")
			elif first_string == third_string == "--address":
				print("The ip address of the server was already given")
				sys.exit("Please use --help if you need assistance")
			if second_string == third_string == "--dir":
				print("The directory of the file was already given")
				sys.exit("Please use --help if you need assistance")
			elif second_string == third_string == "--file":
				print("The name of the file was already given")
				sys.exit("Please use --help if you need assistance")
			elif second_string == third_string == "--address":
				print("The ip address of the server was already given")
				sys.exit("Please use --help if you need assistance")
			if third_string == "--dir":
				try:
					filepath = str(sys.argv[8])
				except IndexError:
					print("The given path was invalid")
					sys.exit("Please use --help if you need assistance")
			elif third_string == "--file":
				try:
					filename = str(sys.argv[8])
				except IndexError:
					print("The given name of the file was invalid")
					sys.exit("Please use --help if you need assistance")
			elif third_string == "--address":
				try:
					server_address = str(sys.argv[8])
				except IndexError:
					print("The given ip address was invalid")
					sys.exit("Please use --help if you need assistance")
			else:
				print("The given option was invalid")
				sys.exit("Please use --help if you need assistance")

			if filepath[-1] != "/":
				filepath = filepath + "/"

			if os.path.isdir(filepath) is not True:
				sys.exit("{} is not a valid directory".format(filepath))
			if os.path.exists(filepath + filename) is not True:
				sys.exit("{} does not exist".format(filepath + filename))
			if re.search(regex, server_address) is None:
				sys.exit("{} is an invalid ip address".format(server_address))

			s = socket.socket()
			s.settimeout(5)
			try:
				s.connect((server_address, 9999))
			except socket.error as exc:
				sys.exit("Caught exception socket.error : {}".format(exc))
			s.send(filename.encode("utf-8"))
			time.sleep(1)
			f = open(filepath + filename, "rb")
			print("Sending {}...".format(filename))
			l = f.read(1024)
			while l:
				s.send(l)
				l = f.read(1024)
			f.close()
			s.close()

		except IndexError:
			print("You need to specify the address of the server, the directory and the name of the file you want to share")
			sys.exit("Please use --help if you need assistance")
	elif selected_mode == "multi":
		try:
			first_string = str(sys.argv[3]).lower()
			if first_string == "--dir":
				try:
					filepath = str(sys.argv[4])
				except IndexError:
					print("The given path was invalid")
					sys.exit("Please use --help if you need assistance")
			elif first_string == "--file":
				print("You do not have to specify the name of the files that you want to send")
				sys.exit("Please use --help if you need assistance")
			elif first_string == "--address":
				try:
					server_address = str(sys.argv[4])
				except IndexError:
					print("The given ip address was invalid")
					sys.exit("Please use --help if you need assistance")
			else:
				print("The given option was invalid")
				sys.exit("Please use --help if you need assistance")

			second_string = str(sys.argv[5]).lower()
			if first_string == second_string == "--dir":
				print("The directory of the file was already given")
				sys.exit("Please use --help if you need assistance")
			elif first_string == second_string == "--address":
				print("The ip address of the server was already given")
				sys.exit("Please use --help if you need assistance")
			if second_string == "--dir":
				try:
					filepath = str(sys.argv[6])
				except IndexError:
					print("The given path was invalid")
					sys.exit("Please use --help if you need assistance")
			elif second_string == "--file":
				print("You do not have to specify the name of the files that you want to send")
				sys.exit("Please use --help if you need assistance")
			elif second_string == "--address":
				try:
					server_address = str(sys.argv[6])
				except IndexError:
					print("The given ip address was invalid")
					sys.exit("Please use --help if you need assistance")
			else:
				print("The given option was invalid")
				sys.exit("Please use --help if you need assistance")

			if filepath[-1] != "/":
				filepath = filepath + "/"

			if os.path.isdir(filepath) is not True:
				sys.exit("{} is not a valid directory".format(filepath))
			if re.search(regex, server_address) is None:
				sys.exit("{} is an invalid ip address".format(server_address))

			for filename in os.listdir(filepath):
				s = socket.socket()
				s.settimeout(5)
				try:
					s.connect((server_address, 9999))
				except socket.error as exc:
					sys.exit("Caught exception socket.error : {}".format(exc))
				s.send(filename.encode("utf-8"))
				time.sleep(1)
				f = open(filepath + filename, "rb")
				print("Sending {}...".format(filename))
				l = f.read(1024)
				while l:
					s.send(l)
					l = f.read(1024)
				f.close()
				s.close()

		except IndexError:
			print("You need to specify the address of the server, the directory and the name of the file you want to share")
			sys.exit("Please use --help if you need assistance")
	elif selected_mode == "zip":
		try:
			first_string = str(sys.argv[3]).lower()
			if first_string == "--dir":
				try:
					filepath = str(sys.argv[4])
				except IndexError:
					print("The given path was invalid")
					sys.exit("Please use --help if you need assistance")
			elif first_string == "--file":
				print("You do not have to specify the name of the files that you want to send")
				sys.exit("Please use --help if you need assistance")
			elif first_string == "--address":
				try:
					server_address = str(sys.argv[4])
				except IndexError:
					print("The given ip address was invalid")
					sys.exit("Please use --help if you need assistance")
			else:
				print("The given option was invalid")
				sys.exit("Please use --help if you need assistance")

			second_string = str(sys.argv[5]).lower()
			if first_string == second_string == "--dir":
				print("The directory of the file was already given")
				sys.exit("Please use --help if you need assistance")
			elif first_string == second_string == "--address":
				print("The ip address of the server was already given")
				sys.exit("Please use --help if you need assistance")
			if second_string == "--dir":
				try:
					filepath = str(sys.argv[6])
				except IndexError:
					print("The given path was invalid")
					sys.exit("Please use --help if you need assistance")
			elif second_string == "--file":
				print("You do not have to specify the name of the files that you want to send")
				sys.exit("Please use --help if you need assistance")
			elif second_string == "--address":
				try:
					server_address = str(sys.argv[6])
				except IndexError:
					print("The given ip address was invalid")
					sys.exit("Please use --help if you need assistance")
			else:
				print("The given option was invalid")
				sys.exit("Please use --help if you need assistance")

			if filepath[-1] != "/":
				filepath = filepath + "/"

			if os.path.isdir(filepath) is not True:
				sys.exit("{} is not a valid directory".format(filepath))
			if re.search(regex, server_address) is None:
				sys.exit("{} is an invalid ip address".format(server_address))

			s = socket.socket()
			s.settimeout(5)
			try:
				s.connect((server_address, 9999))
			except socket.error as exc:
				sys.exit("Caught exception socket.error : {}".format(exc))

			file_paths = retrieve_file_paths(filepath)
			filename = os.path.basename(os.path.normpath(filepath)) + ".zip"
			print("Compressing {}...".format(filename))
			zip_file = zipfile.ZipFile(filename, "w")
			with zip_file:
				for file in file_paths:
					zip_file.write(file)

			zip_file.close()
			s.send(filename.encode("utf-8"))
			time.sleep(1)
			f = open(filename, "rb")
			print("Sending {}...".format(filename))
			l = f.read(1024)
			while l:
				s.send(l)
				l = f.read(1024)
			f.close()
			s.close()
			os.remove(filename)
		except IndexError:
			print("You need to specify the address of the server, the directory and the name of the file you want to share")
			sys.exit("Please use --help if you need assistance")
	else:
		print("Given mode was invalid")
		sys.exit("Please use --help if you need assistance")
