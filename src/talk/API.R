function(userLine,history,category) {
	PYTHON_ANSWER_DIR = "../../talk"
	#PYTHON_ANSWER_DIR = "."
	PYTHON_ANSWER_PATH = paste(PYTHON_ANSWER_DIR,"/answer.py",sep="")
	require(rPython)
	python.load(PYTHON_ANSWER_PATH)
	ans <- python.call("getAnswer",userLine,history,category)
	strsplit(strsplit(ans,":")[[1]][3],",")[[1]][1]
}
