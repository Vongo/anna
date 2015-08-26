require(rjson)
require(ggplot2)

# We read the enriched data
aa <- fromJSON(file="../movies-categorization/outputs/allMovies.json")
longueur <- length(aa)

columnNames <- c("Title","Country","imdbRating","Director","Actors","Year","Genre","Runtime","imdbVotes")

# We create a data.frame representation of this data. Note that the variables are already known.
yy <- sapply(columnNames, function(c) {
    sapply(1:longueur, function(m) {
        aa[[m]][c]
    })
})

xx <- data.frame(yy, stringsAsFactors=F)

movieNames <- xx$Title
rownames(xx) <- movieNames

# We do a bit of formatting.
xx$Runtime <- sapply(xx$Runtime, function(x) as.numeric(strsplit(x, " ")[[1]][1]))
xx$Year <- sapply(xx$Year, function(x) as.numeric(strsplit(x, "–")[[1]][1]))
xx$imdbRating <- as.numeric(xx$imdbRating)
xx$imdbVotes <- as.numeric(xx$imdbVotes)

# Creates a cooccurrence matrix between semantic units
# - units are the semantic units for which we want to know the cooccurrences
# - liste is the liste of semantic observations for which units can cooccur
cooccurrences <- function(units, liste) {
    amtx <- matrix(0, length(units), length(units), dimnames=list(units, units))
    for (elem in liste) {
        elem <- as.vector(elem)
        taille <- length(elem)
        for (i in 1:taille) {
            u1 <- elem[i]
            if (i<taille)
                for (j in (i+1):taille) {
                    u2 <- elem[j]
                    amtx[u1,u2] <- amtx[u1,u2] + 1
                }
        }
    }
    amtx
}

# Describe the topology of the data
# Distribution of the main variables

png("./results/distRatings.png",height=360,width=480)
hist(xx$imdbRating, xlab="Distribution of ratings")
dev.off()

png("./results/distYears.png",height=360,width=480)
hist(xx$Year, xlab="Distribution of movies in time")
dev.off()

png("./results/distRuntime.png",height=360,width=480)
hist(xx$Runtime, xlab="Distribution of movie runtimes")
dev.off()

png("./results/distNbVotes.png",height=360,width=480)
hist(xx$imdbVotes, xlab="Distribution of amount of votes")
dev.off()

# Cooccurrence genres
genreBmovie <- lapply(movieNames, function(m) {
    l_genres <- xx[m,"Genre"]$Title
    unlist(strsplit(l_genres, ", "))
})
names(genreBmovie) <- movieNames
genres <- unique(unlist(genreBmovie))
coocGenre <- cooccurrences(genres,genreBmovie)
write.table(coocGenre, "./results/coocGenre.csv", col.names=T, row.names=T, sep=";")

# Genre Distribution
png("./results/distGenres.png",height=1200,width=1680)
x <- barplot(summary(as.factor(unlist(genreBmovie))))
dev.off()

# Cooccurrence actors
acteurBmovie <- lapply(movieNames, function(m) {
    l_acteur <- xx[m,"Actors"]$Title
    unlist(strsplit(l_acteur, ", "))
})
names(acteurBmovie) <- movieNames
acteurs <- unique(unlist(acteurBmovie))
coocActeurs <- cooccurrences(acteurs,acteurBmovie)
write.table(coocActeurs, "./results/coocActeurs.csv", col.names=T, row.names=T, sep=";")

# Cooccurrence Country
countryBmovie <- lapply(movieNames, function(m) {
    l_countrys <- xx[m,"Country"]$Title
    unlist(strsplit(l_countrys, ", "))
})
names(countryBmovie) <- movieNames
countrys <- unique(unlist(countryBmovie))
coocCountry <- cooccurrences(countrys,countryBmovie)
write.table(coocCountry, "./results/coocCountry.csv", col.names=T, row.names=T, sep=";")

# Average rating by country
rateBcountry <- sapply(countrys, function(c) {
    grades <- xx[grepl(c,xx$Country),"imdbRating"]
    grades <- grades[complete.cases(grades)]
    ifelse(length(grades)>1, mean(grades), NA)
})
names(rateBcountry) <- countrys
rateBcountry <- rateBcountry[order(rateBcountry)]
rateBcountry <- rateBcountry[!is.na(rateBcountry)]

png("./results/rateByCountry.png",height=360,width=480)
x <- barplot(rateBcountry, xaxt="n")
labs <- names(rateBcountry)
text(cex=1, x=x, y=-0.25, labs, xpd=TRUE, srt=35, pos=2)
dev.off()

# Average rating by actor
rateBactor <- sapply(acteurs, function(d) {
    grades <- xx[grepl(d,xx$Actors),"imdbRating"]
    grades <- grades[complete.cases(grades)]
    ifelse(length(grades)>1, mean(grades), NA)
})
names(rateBactor) <- acteurs
rateBactor <- rateBactor[order(rateBactor)]
rateBactor <- rateBactor[!is.na(rateBactor)]

worstActors <- rateBactor[1:10]
png("./results/worstActors.png",height=360,width=480)
x <- barplot(worstActors, xaxt="n")
labs <- names(worstActors)
text(cex=1, x=x, y=-0.25, labs, xpd=TRUE, srt=35, pos=2)
dev.off()

bestActors <- rateBactor[(length(rateBactor)-10):length(rateBactor)]
png("./results/bestActors.png",height=360,width=480)
x <- barplot(bestActors, xaxt="n")
labs <- names(bestActors)
text(cex=1, x=x, y=-0.25, labs, xpd=TRUE, srt=35, pos=2)
dev.off()

# Average rating by director
directorBmovie <- lapply(movieNames, function(m) {
    l_directors <- xx[m,"Director"]$Title
    unlist(strsplit(l_directors, ", "))
})
directors <- unique(unlist(directorBmovie))
rateBdirector <- sapply(directors, function(d) {
    grades <- xx[grepl(d,xx$Director),"imdbRating"]
    grades <- grades[complete.cases(grades)]
    ifelse(length(grades)>1, mean(grades), NA)
})
names(rateBdirector) <- directors
rateBdirector <- rateBdirector[order(rateBdirector)]
rateBdirector <- rateBdirector[!is.na(rateBdirector)]

worstDirectors <- rateBdirector[1:10]
png("./results/worstDirectors.png",height=360,width=480)
x <- barplot(worstDirectors, xaxt="n")
labs <- names(worstDirectors)
text(cex=1, x=x, y=-0.25, labs, xpd=TRUE, srt=35, pos=2)
dev.off()

bestDirectors <- rateBdirector[(length(rateBdirector)-10):length(rateBdirector)]
png("./results/bestDirectors.png",height=360,width=480)
x <- barplot(bestDirectors, xaxt="n")
labs <- names(bestDirectors)
text(cex=1, x=x, y=-0.25, labs, xpd=TRUE, srt=35, pos=2)
dev.off()

# Average rating by year
rateByear <- tapply(xx$imdbRating, xx$Year, mean)
years <- unique(xx$Year)

fit <- lm(rateByear ~ years)

png("./results/ratingEvolution.png",height=360,width=480)
plot(years, rateByear)
abline(fit)
dev.off()

# Average rating by genre
rateBgenre <- sapply(genres, function(d) {
    grades <- xx[grepl(d,xx$Genre),"imdbRating"]
    grades <- grades[complete.cases(grades)]
    ifelse(length(grades)>1, mean(grades), NA)
})
names(rateBgenre) <- genres
rateBgenre <- rateBgenre[order(rateBgenre)]
rateBgenre <- rateBgenre[!is.na(rateBgenre)]

png("./results/rateByGenre.png",height=360,width=480)
x <- barplot(rateBgenre, xaxt="n")
labs <- names(rateBgenre)
text(cex=1, x=x, y=-0.25, labs, xpd=TRUE, srt=35, pos=2)
dev.off()

# Average rating by runtime
fit <- lm(xx$imdbRating ~ xx$Runtime)
png("./results/ratingPerRuntime.png",height=360,width=480)
plot(xx$Runtime,xx$imdbRating)
abline(fit)
dev.off()

# Average rating by number of votes
Data <- xx[,c("imdbRating","imdbVotes")]
names(Data) <- c("y","x")
Data <- Data[complete.cases(Data),]
png("./results/ratingPerNbVotes.png",height=360,width=480)
ggplot(Data, aes(x,y)) + geom_point() + geom_smooth()
dev.off()

# Average runtime by genre
dureeBgenre <- sapply(genres, function(d) {
    duration <- xx[grepl(d,xx$Genre),"Runtime"]
    duration <- duration[complete.cases(duration)]
    ifelse(length(duration)>1, mean(duration), NA)
})
names(dureeBgenre) <- genres
dureeBgenre <- dureeBgenre[order(dureeBgenre)]
dureeBgenre <- dureeBgenre[!is.na(dureeBgenre)]

png("./results/dureeByGenre.png",height=360,width=480)
x <- barplot(dureeBgenre, xaxt="n")
labs <- names(dureeBgenre)
text(cex=1, x=x+0.75, y=-0.75, labs, xpd=TRUE, srt=45, pos=2)
dev.off()

# Nombre de films par genre par année
    nGenres <- length(genres)
    zz <- xx[!is.na(xx$Year)&!is.na(xx$imdbRating),]

    # get the range for the x and y axis
    xrange <- range(zz$Year)
    yrange <- range(zz$imdbRating)

    png(paste("./results/NoteBgenre.png",sep=""))

    # set up the plot
    plot(xrange, yrange, type="n", xlab="Année", ylab="Note moyenne")
    colors <- rainbow(nGenres)
    linetype <- 1:nGenres
    plotchar <- seq(18,18+nGenres,1)

    # add lines
    i <- 1
    for (g in genres) {
        yy <- zz[grepl(g,xx$Genre),]
        lines(yy$Year, yy$imdbRating, type="b", lwd=1.5,
            lty=linetype[i], col=colors[i], pch=plotchar[i])
        i + 1 -> i
    }

    # add a title and subtitle
    title(paste("",sep=""))

    # add a legend
    legend("topleft", genres, genres, cex=0.8, col=colors,
        pch=plotchar, lty=linetype, title="Genre")

    dev.off()
