install.packages(c('tidyverse', 'car', 'bootstrap', 'haven', 'psych','foreign'))
library(psych)
library(readr)
library(tidyverse)
library("foreign")


gender <- subset(gss, select = c(id, year, fehome, fework, fepres, fepol, 
                    fefam, fehelp, fechld,fepresch, age, sex, educ, partyid))
table(gender$FEHOME)

write.csv(gender, "gender.csv")



gender = read.csv("gender.csv")


gender = gender %>%
  mutate(fehome = dplyr::recode(fehome, "1" = -.5, "2" = .5)) %>%
  mutate(fework = dplyr::recode(fework, "1" = .5, "2" = -.5)) %>%
  mutate(fepres = dplyr::recode(fepres, "1" = .5, "2" = -.5)) %>%
  mutate(fepol = dplyr::recode(fepol, "1" = -.5, "2" = .5)) %>%
  mutate(fefam = dplyr::recode(fefam, "1" = -1.5, "2" = -.5, "3" = .5, "4" = 1.5)) %>%
  mutate(fehelp = dplyr::recode(fehelp, "1" = -1.5, "2" = -.5, "3" = .5, "4" = 1.5)) %>%
  mutate(fechld = dplyr::recode(fechld, "1" = 1.5, "2" = .5, "3" = -.5, "4" = -1.5)) %>%
  mutate(fepresch = dplyr::recode(fepresch, "1" = -1.5, "2" = -.5, "3" = .5, "4" = 1.5))
  
gender[1:11] <- lapply(gender[1:11], as.numeric)
describe(gender[3:10])


sapply(gender[3:11], function(cl) list(means=mean(cl,na.rm=TRUE), sds=sd(cl,na.rm=TRUE)))


#TO DO: age & SEX
gender[1:11] <- lapply(gender[1:11], as.numeric)

year <- gender %>% group_by(year) %>% summarize(fehome = mean(fehome, na.rm = TRUE), 
                                                fework = mean(fework, na.rm = TRUE),
                                                fepres = mean(fepres, na.rm = TRUE),
                                                fepol = mean(fepol, na.rm = TRUE),
                                                fefam = mean(fefam, na.rm = TRUE),
                                                fehelp = mean(fehelp, na.rm = TRUE),
                                                fechld = mean(fechld, na.rm = TRUE),
                                                fepresch = mean(fepresch, na.rm = TRUE))

year$sum1 <- rowMeans(year[2:5], na.rm = TRUE)
year$sum2 <- rowMeans(year[6:9], na.rm = TRUE)
year$sum_total <- rowMeans(year[10:11], na.rm = TRUE)

write.csv(year, "gss.csv")
write.csv(year, "gss_sum.csv")

#_____________IPUSM____________
library(dplyr)
library(tidyr)
labor <- read.csv("ipums.csv",header=TRUE, encoding = "UTF-8")
str(labor)
table(labor$Single.words)

occup <- labor %>% group_by(YEAR, SEX,Single.words) %>% 
  summarise(count = n())


range <- occup[occup$YEAR >= 1972 & occup$YEAR <= 2008,] 


library(tidyr)

range = range %>% ungroup() %>% complete(YEAR, SEX, Single.words, fill = list(count = 0))


percent <- range %>% group_by(YEAR, Single.words) %>% 
  mutate(percent = (count[SEX == 2]-count[SEX == 1])/sum(count) * 100)

write.csv(percent, "IPUMS.csv")

library(psych)
table(labor$YEAR)

head(labor)
cor(new$attitude, new$occupation)



install.packages(ggplot2)
library(ggplot2)

ggplot(new, aes(x=YEAR)) + 
  geom_line(aes(y = fehome), color = "darkred") + 
  geom_line(aes(y = fework), color="blue") +
  geom_line(aes(y = fepres), color="green") +
  geom_line(aes(y = fepol), color="yellow")

plot(new$YEAR, new$fehome, type="b", col="green", lwd=5, 
     xlab="year", ylab="Do you agree or disagree with this statement?  ", 
     main=" Women should take care of running their homes and leave running the country up to men.",
     font.main=2, font.lab=4, font.sub=4)
?plot
?plot
library(ggplot2)
plot(fehome)


table(data$FEHOME)
str(data$FEHOME)

(length(which(data$FEHOME == "AGREE"))-length(which(data$FEHOME == "DISAGREE")))/length(data$FEHOME)

length(data$FEHOME)

mean(as.numeric(data$FEHOME), na.rm=TRUE)
