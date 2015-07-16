function() {
	CONNECT_DIR = "../../neoServer"
	PYTHON_CONNECT_PATH = paste(CONNECT_DIR,"/connect.py",sep="")
	require(rPython)
	python.load(PYTHON_CONNECT_PATH)
	ans <- python.call("disconnect")
}
