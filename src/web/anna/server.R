library(rPython)
library(rjson)

PYTHON_ANSWER_DIR = "../../talk"
PYTHON_ANSWER_PATH = paste(PYTHON_ANSWER_DIR,"/answer.py",sep="")
CONNECT_PATH = "../../neoServer/connect.R"
DISCONNECT_PATH = "../../neoServer/disconnect.R"
API_PATH = "../../talk/API.R"
CATEGORIES_PATH = "../../pre-processing/movies-categorization/outputs/categories.json"
TESTMODE = NULL

# Creates a Shiny server
shinyServer(function(input, output, session) {

	HISTORY = vector() # Each item is an utterance from Anna or the user.
	USER_NAME = NULL # User name, once it is set. It is stored to avoid requesting it all the time.
	userNameSet = F # True once the user name has been set once.
	newLineReady = F # True when it is time for Anna to answer.

	# Connects to the Neo4j Database.
	source(CONNECT_PATH,chdir=T)$value()

	# formulates a user quote on the format "\textbf{TIME, USERNAME said} : {QOUTE}"
	formulate <- function(user, quote) {
		paste("<b>",as.character(Sys.time()),", ",user," said</b> : ",quote, sep="")
	}

	# Given an utterance, replaces ANNA, USERNAME and EASTER macros by proper names.
	replace.names <- function(sentence) {
		replace.username <- function(sentence, rep=input$userName) {
			if (grepl("USERNAME", sentence)){
				dec <- strsplit(sentence,"USERNAME")
				left <- dec[[1]][1]
				right <- dec[[1]][2]
				paste(left,rep,right,sep="")
			}
			else sentence
		}
		replace.anna <- function(sentence, rep="Anna") {
			if (grepl("ANNA", sentence)){
				dec <- strsplit(sentence,"ANNA")
				left <- dec[[1]][1]
				right <- dec[[1]][2]
				paste(left,rep,right,sep="")
			}
			else sentence
		}
		replace.easter <- function(sentence, rep="Behrang") {
			if (grepl("EASTER", sentence)){
				dec <- strsplit(sentence,"EASTER")
				left <- dec[[1]][1]
				right <- dec[[1]][2]
				paste(left,rep,right,sep="")
			}
			else sentence
		}

		replace.username(replace.anna(replace.easter(sentence)))
	}

	# Calls R API for calling answering engine and formats the answer.
	anna.answers <- function(userLine) {
		answer <- source(API_PATH,chdir=T)$value(userLine,input$categories)
		answer <- replace.names(answer)
		newLine <- formulate("ANNA", answer)
		HISTORY <<- c(HISTORY, newLine)
	}

	# Gets Python hi variable (a basic list) from hello.py, and formats it.
	anna.says.hi <- function() {
		python.load(paste(PYTHON_ANSWER_DIR,"/hello.py",sep=""))
		answer <- sample(python.get("hi"),1)
		answer <- replace.names(answer)
		newLine <- formulate("ANNA", answer)
		HISTORY <<- c(HISTORY, newLine)
	}

	# Switches tab (to conversation) when username is set.
	observe({
		if (input$validateUserName == 0)
			return()
		if (input$userName != "") {
			userNameSet <<- T
			USER_NAME <<- input$userName
			updateTabsetPanel(session, "tabs", selected = "Chat")
		}
	})

	# Checks if user spoke. In this case, it's Anna's turn.
	observe({
		if (input$userSpoke == 0)
			return()
		newLineReady <<- T
	})

	# Switches tab whenever user tries to get back to user details if username is already set.
	observe({
		if (input$tabs == "User Detail") {
			if (userNameSet)
				updateTabsetPanel(session, "tabs", selected = "Chat")
		}
	})

	# Checks whether the user wants to evaluate Anna's answers.
	observe({
		switch(input$testMode,
			"1" = {TESTMODE <<- T},
			"2" = {TESTMODE <<- F},
			{print("TestMode not set.")}
		)
	})

	# Checks if the user asked to disconnect from the chatting server.
	observe({
		if (input$Disconnect == 0)
			return()
		# Disconnects the user from the Neo4j Server.
		source(DISCONNECT_PATH,chdir=T)$value()
		Disconnecting(forceKill666) #This will raise an exception and crash the server. Who said "dirty" ?
	})

	# Displays Movie Categories combo box.
	output$temp <- renderUI({
		categories <- fromJSON(file=CATEGORIES_PATH)
		selectInput("categories","Categories",names(categories))
	})

	# Checks whether Anna needs to speak, calls the proper method and displays the history.
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

	# Displays evaluation tool if asked.
	output$evaluation <- renderUI({
		input$userSpoke
		if (TESTMODE)
			sliderInput("eval", "How would you evaluate Anna's last answer ?", 0, 5, 3, step = 1)
	})

	# Wipes the user textbox when the latter just spoke.
	output$input <- renderUI({
		input$userSpoke
		textInput("userInput","")
	})
})
