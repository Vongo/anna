function(userLine,category) {
	# Loads rPython library and calls the getAnswer Python method with proper parameters.
	PYTHON_ANSWER_DIR = "../../talk"
	PYTHON_ANSWER_PATH = paste(PYTHON_ANSWER_DIR,"/answer.py",sep="")
	require(rPython)
	python.load(PYTHON_ANSWER_PATH)
	python.call("getAnswer",userLine,category)
}
