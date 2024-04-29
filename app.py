from santazip import SantaZip
import base64




def brute_force_attack(wordlist_path):

    with open(wordlist_path, "r") as wordlist:

        for password in wordlist:

        	password = password.strip()

        	zip_object = SantaZip("flag.txt", "flag.zip", password)

        	try:

        		print(zip_object.decrypt_zip_file())
        	except Exception as e:
        		
        		continue

				# print(zip_object.generate_zip_file())


brute_force_attack("/usr/share/wordlists/rockyou.txt")

