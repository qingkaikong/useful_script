#First time you need install some packages
#install.packages("AppliedPredictiveModeling")
#install.packages("caret")
#install.packages("minerva")
#install.packages("CORElearn")
#install.packages("pROC")
library(pROC)
library(AppliedPredictiveModeling)
library(caret)
library(CORElearn)
library(minerva)

#load the solubility data
data(solubility)

                      ###########   Numeric Outcomes   ###########
################################Correlation method####################################
#get the correlation between the predictor and response
cor(solTrainXtrans$NumCarbon, solTrainY)

#use the apply function to get all the predictors
#determine which columns have teh string "FP" in teh name and exclude these to get the numeric predictors
fpCols <- grepl("FP", names(solTrainXtrans))
#exclude these to get only the numeric predictor names
numericPreds <- names(solTrainXtrans)[!fpCols]
#using apply function to calculate the correlation
corrValues <- apply(solTrainXtrans[,numericPreds], MARGIN = 2, FUN = function(x,y) cor(x,y), y = solTrainY)
head(corrValues)
#to get the rank correlation, use the method = "spearman"
rank_corrValues = apply(solTrainXtrans[,numericPreds], MARGIN = 2, FUN = function(x,y) cor(x,y, method = "spearman"), y = solTrainY)

################################LOESS method####################################
smoother <- loess(solTrainY~solTrainXtrans$NumCarbon)
smoother
#plot it out using function from lattice in caret
xyplot(solTrainY~solTrainXtrans$NumCarbon, type=c("p", "smooth"), xlab = "# Carbons", ylab = "Solubility")

#the caret function filterVarImp with the nonpara = TRUE option (for non-parametric regression) creates
#a LOESS model for each predictor and quantifies the relationship with the outcome
loessResults <- filterVarImp(x=solTrainXtrans[,numericPreds], y=solTrainY, nonpara=TRUE)
loessResults

################################ MIC method####################################
#the minerva package can be used to calculate the MIC statistics between the predictors and outcomes
micValues <- mine(solTrainXtrans[,numericPreds], solTrainY)
#several statistics are calculated
names(micValues)
head(micValues$MIC)

################################ t-test method####################################
#for categorical predictors, the simple t.test function computes the difference in means and the p-value
t.test(solTrainY~solTrainXtrans$FP044)
?t.test

#This approach can be extended to all predictors using apply function
getTstats <- function(x,y)
  {tTest <- t.test(y~x)
   out <- c(tStat = tTest$static, p=tTest$p.value)
   out
  }

tVals <- apply(solTrainXtrans[,fpCols], MARGIN = 2, FUN = getTstats, y-solTrainY)
#swtich the dimensions
tVals <-t(tVals)
head(tVals)

###########   Categorical Outcomes   ###########
################################ROC method####################################
data(segmentationData)

cellData <- subset(segmentationData, Case == 'Train')
cellData$Case <- cellData$Cell <- NULL
#the class is in the first column
head(names(cellData))
rocValues <- filterVarImp(x=cellData[,-1], y=cellData$Class)
#Column is created for each class
head(rocValues)

################################Relief method####################################
reliefValues <- attrEval(Class~., data=cellData, estimator = "ReliefFequalK", ReliefIterations=50)
head(reliefValues)

#ReliefF
perm <- permuteRelief(cellData[,-1], y=cellData$Class, nperm=500, estimator = "ReliefFequalK", ReliefIterations=50)
head(perm$permutations)

histogram(~value|Predictor, data=perm$permutations)

################################ MIC method####################################
#the MIC statistic can be computed as before but with a binary dummy variable encoding of the classes
micValues <- mine(x=cellData[,-1], y=ifelse(cellData$Class=='PS', 1,0))
head(micValues$MIC)
