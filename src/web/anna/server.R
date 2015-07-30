library(rPython)
library(rjson)

PYTHON_ANSWER_DIR = "../../talk"
PYTHON_ANSWER_PATH = paste(PYTHON_ANSWER_DIR,"/answer.py",sep="")
CONNECT_PATH = "../../neoServer/connect.R"
DISCONNECT_PATH = "../../neoServer/disconnect.R"
API_PATH = "../../talk/API.R"
CATEGORIES_PATH = "../../pre-processing/movies-categorization/outputs/categories.json"
TESTMODE = NULL

shinyServer(function(input, output, session) {

	HISTORY = vector()
	USER_NAME = NULL
	userNameSet = F
	newLineReady = F
	firstChatLoad = T

	source(CONNECT_PATH,chdir=T)$value()

	formulate <- function(user, quote) {
		paste("<b>",as.character(Sys.time()),", ",user," said</b> : ",quote, sep="")
	}

	anna.answers <- function(userLine, history=NULL) {
		# python.load(PYTHON_ANSWER_PATH)
		# answer <- sample(python.get("answer"),1)

		answer <- source(API_PATH,chdir=T)$value(userLine,input$categories)

		newLine <- formulate("ANNA", answer)
		HISTORY <<- c(HISTORY, newLine)
	}

	anna.says.hi <- function() {
		python.load(paste(PYTHON_ANSWER_DIR,"/test.py",sep=""))
		answer <- sample(python.get("hi"),1)
		newLine <- formulate("ANNA", answer)
		HISTORY <<- c(HISTORY, newLine)
	}

	observe({
		if (input$validateUserName == 0)
			return()
		if (input$userName != "") {
			userNameSet <<- T
			USER_NAME <<- input$userName
			updateTabsetPanel(session, "tabs", selected = "Chat")
		}
	})

	observe({
		if (input$userSpoke == 0)
			return()
		newLineReady <<- T
	})

	observe({
		if (input$tabs == "User Detail") {
			if (userNameSet)
				updateTabsetPanel(session, "tabs", selected = "Chat")
		}
	})

	observe({
		switch(input$testMode,
			"1" = {TESTMODE <<- T},
			"2" = {TESTMODE <<- F},
			{print("TestMode not set.")}
		)
	})

	observe({
		if (input$Disconnect == 0)
			return()
		source(DISCONNECT_PATH,chdir=T)$value()
		Disconnecting(forceKill666) #This will raise an exception and crash the server. Who said "dirty" ?
	})

	output$temp <- renderUI({
		categories <- fromJSON(file=CATEGORIES_PATH)
		selectInput("categories","Categories",names(categories))
	})

	output$history <- renderUI({
		if (input$userSpoke == 0){
			anna.says.hi()
		} else if (newLineReady) {
			newLine <- formulate(USER_NAME, input$userInput)
			HISTORY <<- c(HISTORY, newLine)
			anna.answers(input$userInput)
			newLineReady <<- F
		}
		HTML(paste(HISTORY, collapse="<br/>"))
	})

	output$evaluation <- renderUI({
		input$userSpoke
		if (TESTMODE)
			sliderInput("eval", "How would you evaluate Anna's last answer ?", 0, 5, 3, step = 1)
	})

	output$input <- renderUI({
		input$userSpoke
		textInput("userInput","")
	})
})
