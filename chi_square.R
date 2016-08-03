#read in the data
data<-read.csv("combined_final_codes_sim-5-29topics.csv")

data.chi <- data.frame()
for (j in c(7,8,10,11)) { # for each of the four strategy columns
  # identify strategy based on our outer loop index
  strategy <- "none" # default, nothing should be "none"
  strat <- -1 # TODO: DataFrame shouldn't need all cols to be scalar, but it does?
  
  if(j==7) {
    strategy <- "comp.crit"
    strat <- 1
  }
  else if (j==8) {
    strategy <- "strategy"
    strat <- 2
  }
  else if (j==10) {
    strategy <- "combined.calculated.strategy"
    strat <- 3
  }
  else if (j==11) {
    strategy <- "combined.strategy"
    strat <- 4
  }
  print(paste("Analyzing ",strategy," (",strat,") strategy codings vs. numTopics", sep=""))
  
  # loop through each numTopic columns
  for (i in 14:83) { 
    if (!i %% 2) { # only do something when the numTopic col index is even (the topic cols are even numbers)
      topic_col <- (i/2)-2 # calculate actual number of topics from column number

      # perform chi-square test on j and i columns
      chi_eval <- chisq.test(data[,j], data[,i])
      data.chi <- rbind(data.chi, c(strat,topic_col,chi_eval$statistic, chi_eval$p.value, chi_eval$parameter, chi_eval$residuals))
      
      # printing debug messages to console
      #print(paste("STRATEGY:",strategy," COLUMN:topic ",topic_col)) 
      #print(paste("X-sq: ", chi_eval$statistic, "p-value: ",chi_eval$p.value))
    }
  }
  # printing to file
  colnames(data.chi) <- c("ind","strategy_coding", "numTopics","chi_sq_stat","p_value","DoF","residuals_pearson")
  write.table(data.chi, file = "chi_squared.csv",sep = ",")
}
