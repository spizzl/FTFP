



def byte(text):
	return bytes(text.rstrip(), "utf8")

def string(bytes):
	return(str(bytes, "utf8")).rstrip()
