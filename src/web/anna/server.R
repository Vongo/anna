library(rPython)
library(rjson)

PYTHON_ANSWER_PATH = "../../talk/test.py"
CATEGORIES_PATH = "../../movies-categorization/outputs/categories.json"

shinyServer(function(input, output, session) {

	HISTORY = vector()
	USER_NAME = NULL
	userNameSet = F
	newLineReady = F

	anna.answers <- function() {
		python.load(PYTHON_ANSWER_PATH)
		answer <- sample(python.get("answer"),1)
		newLine <- paste(as.character(Sys.time()),"ANNA said :",answer)
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

	output$temp <- renderUI({
		print(getwd())
		categories <- fromJSON(file=CATEGORIES_PATH)
		selectInput("categories","Categories",names(categories))
	})

	output$history <- renderUI({
		if (input$userSpoke == 0)
			return()
		if (newLineReady) {
			newLine <- paste(as.character(Sys.time()),USER_NAME,"said :",input$userInput)
			HISTORY <<- c(HISTORY, newLine)
			anna.answers()
			newLineReady <<- F
		}
		HTML(paste(HISTORY, collapse="<br/>"))
	})
})
