library(shiny)
shinyUI(
	fluidPage(
		titlePanel("ANNA"),
		sidebarLayout(
			position="left",
			mainPanel(
				tabsetPanel(
					id="tabs",
					tabPanel(
						title="User Detail",
						fluidRow(h3("  Nickname"),
							column(2,
								textInput("userName","")
							),
							column(1,
								actionButton("validateUserName", "Ok !")
							)
						),
						fluidRow(
							column(3,
								radioButtons("testMode", label = h3("Test Mode"),
        							choices = list("I want to evaluate Anna's answers" = 1, 
        							"I just want to interact" = 2), 
        							selected = 2
        						)
							)
						)
					),
					tabPanel(
						title="Chat",
						fluidRow(
							column(8,
								htmlOutput("history")
							)
						),
						fluidRow(
							h5(" Answer Anna :")
						),
						fluidRow(
							column(4,
								htmlOutput("input")
							),
							column(1,
								actionButton("userSpoke", "Speak")
							),
							column(5,
								htmlOutput("evaluation")
							)
						)
					)
				)
			),
			sidebarPanel(
				uiOutput("temp")
			)
		)
	)
)
