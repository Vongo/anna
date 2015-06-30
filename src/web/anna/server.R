library(rPython)
library(rjson)

PYTHON_ANSWER_PATH = "../../talk/test.py"
CATEGORIES_PATH = "../../pre-processing/movies-categorization/outputs/categories.json"
TESTMODE = NULL

shinyServer(function(input, output, session) {

	HISTORY = vector()
	USER_NAME = NULL
	userNameSet = F
	newLineReady = F
	firstChatLoad = T

	formulate <- function(user, quote) {
		paste("<b>",as.character(Sys.time()),", ",user," said</b> : ",quote, sep="")
	}

	anna.answers <- function() {
		python.load(PYTHON_ANSWER_PATH)
		answer <- sample(python.get("answer"),1)
		newLine <- formulate("ANNA", answer)
		HISTORY <<- c(HISTORY, newLine)
	}

	anna.says.hi <- function() {
		python.load(PYTHON_ANSWER_PATH)
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
			anna.answers()
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
