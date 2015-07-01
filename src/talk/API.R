function(userLine,history,category) {
	PYTHON_ANSWER_DIR = "."
	PYTHON_ANSWER_PATH = paste(PYTHON_ANSWER_DIR,"/answer.py",sep="")
	require(rPython)
	python.load(PYTHON_ANSWER_DIR)
	python.call("getAnswer",userLine,history,category)
}
