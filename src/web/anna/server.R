library(rPython)
library(rjson)

PYTHON_ANSWER_PATH = "../test.py"
CATEGORIES_PATH = "src/movies-categorization/outputs/categories.json"

anna.answers <- function() {
	python.load(PYTHON_ANSWER_PATH)
	answer <- python.get("answer")
	newLine <- paste(as.character(Sys.time()),"ANNA said :",answer)
	HISTORY <<- c(HISTORY, newLine)
}

shinyServer(function(input, output, session) {

	HISTORY = vector()
	USER_NAME = NULL
	userNameSet = F
	newLineReady = F

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
		categories <- fromJSON(file=CATEGORIES_PATH)
		selectInput("categories","Categories",names(categories))
	})

	output$history <- renderUI({
		if (input$userSpoke == 0)
			return()
		if (newLineReady) {
			newLine <- paste(as.character(Sys.time()),USER_NAME,"said :",input$userInput)
			HISTORY <<- c(HISTORY, newLine)
			# anna.answers()
			newLineReady <<- F
		}
		HTML(paste(HISTORY, collapse="<br/>"))
	})
})
