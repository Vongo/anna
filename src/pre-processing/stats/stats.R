require(rjson)
require(ggplot2)

aa <- fromJSON(file="../movies-categorization/outputs/allMovies.json")
longueur <- length(aa)

columnNames <- c("Title","Country","imdbRating","Director","Actors","Year","Genre","Runtime","imdbVotes")

yy <- sapply(columnNames, function(c) {
    sapply(1:longueur, function(m) {
        aa[[m]][c]
    })
})

xx <- data.frame(yy, stringsAsFactors=F)

movieNames <- xx$Title
rownames(xx) <- movieNames

xx$Runtime <- sapply(xx$Runtime, function(x) as.numeric(strsplit(x, " ")[[1]][1]))
xx$Year <- sapply(xx$Year, function(x) as.numeric(strsplit(x, "–")[[1]][1]))
xx$imdbRating <- as.numeric(xx$imdbRating)
xx$imdbVotes <- as.numeric(xx$imdbVotes)
xx$Runtime <- as.numeric(xx$Runtime)

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

# Cooccurrence genres
genreBmovie <- lapply(movieNames, function(m) {
    l_genres <- xx[m,"Genre"]$Title
    unlist(strsplit(l_genres, ", "))
})
names(genreBmovie) <- movieNames
genres <- unique(unlist(genreBmovie))
coocGenre <- cooccurrences(genres,genreBmovie)
write.table(coocGenre, "./results/coocGenre.csv", col.names=T, row.names=T, sep=";")

# Cooccurrence acteurs
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

# Note moyenne par pays
rateBcountry <- sapply(countrys, function(d) {
    mean(xx[grepl(d,xx$Country),"imdbRating"])
})
names(rateBcountry) <- countrys
rateBcountry <- rateBcountry[order(rateBcountry)]
rateBcountry <- rateBcountry[!is.na(rateBcountry)]

# Note moyenne par acteur
rateBactor <- sapply(acteurs, function(d) {
    mean(xx[grepl(d,xx$Actors),"imdbRating"])
})
names(rateBactor) <- acteurs
rateBactor <- rateBactor[order(rateBactor)]
rateBactor <- rateBactor[!is.na(rateBactor)]

# Note moyenne par réalisateur
directorBmovie <- lapply(movieNames, function(m) {
    l_directors <- xx[m,"Director"]$Title
    unlist(strsplit(l_directors, ", "))
})
directors <- unique(unlist(directorBmovie))
rateBdirector <- sapply(directors, function(d) {
    mean(xx[grepl(d,xx$Director),"imdbRating"])
})
names(rateBdirector) <- directors
rateBdirector <- rateBdirector[order(rateBdirector)]
rateBdirector <- rateBdirector[!is.na(rateBdirector)]

# Note moyenne par année
rateByear <- tapply(xx$imdbRating, xx$Year, mean)
qplot(names(rateByear),rateByear)

# Note moyenne par genre
rateBgenre <- sapply(genres, function(d) {
    mean(xx[grepl(d,xx$Genre),"imdbRating"])
})
names(rateBgenre) <- genres
rateBgenre <- rateBgenre[order(rateBgenre)]
rateBgenre <- rateBgenre[!is.na(rateBgenre)]

# note/durée
qplot(xx$Runtime,xx$imdbRating)

# note/nombreVotes
qplot(xx$imdbVotes, xx$imdbRating)

# Durée moyenne par genre
dureeBgenre <- sapply(genres, function(d) {
    mean(xx[grepl(d,xx$Genre),"Runtime"])
})
names(dureeBgenre) <- genres
dureeBgenre <- dureeBgenre[order(dureeBgenre)]
dureeBgenre <- dureeBgenre[!is.na(dureeBgenre)]

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
