#Installing the packages
install.packages('readxl')
install.packages('corrplot')

#Libraries used during the analysis
library(readxl)
library(corrplot)

#Deciding the sample
sample(seq(3,86),25)

#Reading the files from Excel
library(readxl)
Test1 <- read_excel("C:/Users/Yousef El-bayoumi/Desktop/Test1.xlsx")
View(Test1)
library(readxl)
Test2 <- read_excel("C:/Users/Yousef El-bayoumi/Desktop/Test2.xlsx")
View(Test2)

#Summary statistics for the data
#Population :
x1 = Test1$PopulationHours
x2 = Test1$PopulationScale
x3 = Test1$PopulationSpend
x4 = Test1$PopulationPlaylists
x5 = Test1$PopulationAge

# Sample:
x6 = Test2$SampleHours
x7 = Test2$SampleScale
x8 = Test2$SampleSpend
x9 = Test2$SamplePlaylists
x10 = Test2$SampleAge
plot(x1,type="h",las=1,bty="o",
     main="How many hours per day do you listen to music?",
     xlab="Population mean=2.515",ylab="Hours")
plot(x2,type="h",las=1,bty="o",
     main="From a 1-100 scale, how much music make you happy?",
     xlab="Population mean=84.31",ylab="Happiness")
plot(x3,type="h",las=1,bty="o",
     main="How much do you spend on music in TL? (subscribes, etc.)",
     xlab="Population mean=16.26",ylab="Spending in TL")
plot(x4,type="h",las=1,bty="o",
     main="How many songs do you have in your own playlists?
approximately",
     xlab="Population mean=94.07",ylab="Songs")
plot(x5,type="h",las=1,bty="o",
     main="What was your age when you started listening to
music much?",
     xlab="Population mean=11.10",ylab="Age")
plot(x6,type="h",las=1,bty="o",
     main="How many hours per day do you listen to music?",
     xlab="Sample mean=2.27",ylab="Hours")
plot(x7,type="h",las=1,bty="o",
     main="From a 1-100 scale, how much music make you happy?",
     xlab="Sample mean=86.6",ylab="Happiness")
plot(x8,type="h",las=1,bty="o",
     main="How much do you spend on music in TL? (subscribes, etc.)",
     xlab="Sample mean=21.16",ylab="Spending in TL")
plot(x9,type="h",las=1,bty="o",
     main="How many songs do you have in your own playlists?
approximately",
     xlab="Sample mean=82.24",ylab="Songs")
plot(x10,type="h",las=1,bty="o",
     main="What was your age when you started listening to
music much?",
     xlab="Sample mean=13.44",ylab="Age")

#Showing the correlation between the data
cor(Test2$SampleSpend, Test2$SampleScale)
cor(Test2$SampleAge, Test2$SampleHours)
cor(Test2$SamplePlaylists, Test2$SampleAge)
cor.test(Test2$SampleSpend, Test2$SampleScale)
cor.test(Test2$SampleAge, Test2$SampleHours)
cor.test(Test2$SamplePlaylists, Test2$SampleAge)
cor(Test2)
cor2 = cor(Test2)
install.packages("corrplot")
require(corrplot)
corrplot(cor2,method = "circle", type = "upper", order = "AOE")
corrplot(cor2,method = "number", type = "upper", order = "AOE")
#Point estimations
mean(x1)
mean(x2)
mean(x3)
mean(x4)
mean(x5)
mean(x6)
mean(x7)
mean(x8)
mean(x9)
mean(x10)
sd(x1)
sd(x2)
sd(x3)
sd(x4)
sd(x5)
sd(x6)
sd(x7)
sd(x8)
sd(x9)
sd(x10)

#Confidence Interval
t.test(Test2$SampleHours, conf.level = 0.95)
shapiro.test(Test2$SampleScale)
t.test(Test2$SampleScale, conf.level=0.99)

#Hypothesis Testing
shapiro.test(Test2$SampleHours)
t.test(Test2$SampleHours,alternative = "greater",mu=1.21)
shapiro.test(Test2$SampleScale)
t.test(Test2$SampleScale,alternative = "greater",mu=65)
shapiro.test(Test2$SampleSpend)
t.test(Test2$SampleSpend,alternative = "less",mu=25)

#Goodness of Fit
Times <- c(10, 14.5, 19, 22.5)
names(Times) <- c("Morning", "Afternoon", "Evening", "Late time")
probability <- c(6/24, 2/24, 7/24, 9/24)
chisq.test(Times, p=probability)

#Modeling
#Simple Linear Regression
plot(y=Test2$SampleHours,x=Test2$SampleScale,
     ylab = "Averagely listening to music per day",
     xlab = "Happiness scale")
cor(Test2$SampleHours,Test2$SampleScale)

#First Model
Model1<-lm(Test2$SampleHours~Test2$SampleScale)
summary(Model1)
plot(Model1,1:2)

#Second Model
Model2<-lm(Test2$SampleHours^0.5~Test2$SampleScale)
summary(Model2)
plot(Model2,1:2)

#Third Model
Model3<-lm(Test2$SampleHours^0.5~I(Test2$SampleScale^0.5))
summary(Model3)
plot(Model3,1:2)