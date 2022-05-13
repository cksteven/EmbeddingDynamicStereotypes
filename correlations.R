library(psych)
library(tidyverse)
library(car)
setwd("/Users/kesong/Documents/git-personal/EmbeddingDynamicStereotypes")
# install.packages("tseries")
library(tseries)

d1 = read.csv("1972-2018atti&occup.csv")
d2 = read.csv("occups_difs.csv", skip=1)

d2 = d2 %>% rename(year = occup)
d2 = d2[d2$year > 1970, ]
d1 = d1[d1$year < 2010, ]

filtered_occups = c('accountant', 'architect', 'artist', 'athlete', 'attendant','author', 'baker', 'broker', 'carpenter', 'cashier', 'clergy','clerical', 'clerk', 'conductor', 'cook', 'dancer', 'dentist','designer', 'driver', 'economist', 'engineer', 'farmer','gardener', 'housekeeper', 'laborer', 'librarian', 'mathematician','midwife', 'musician', 'nurse', 'official', 'operator','photographer', 'pilot', 'police', 'porter', 'professor','psychologist', 'retired', 'sailor', 'scientist', 'secretary','soldier', 'student', 'tailor', 'teacher')
d = d2[,c("year",filtered_occups)]

lag_df = lag_df[(lag_df$max_lag >= -5) & (lag_df$max_lag <= 5),]

mean(lag_df$max_lag)
mean(lag_df$max_acf)

d3 = read.csv("IPUMS.csv") %>% janitor::clean_names()
d3 = d3[d3$sex == 1,] %>% select(-sex, -x) %>% rename(occup = single_words)
d3 = d3[d3$occup %in% filtered_occups,]

occup_stats = d3 %>% pivot_wider(
        id_cols = year,
        names_from = occup,
        values_from = percent)

write.csv(occup_stats, "occup_stats.csv")

occup_stats = occup_stats[occup_stats$year %in% d$year,]
occup_na = c("dancer", "dentist", "designer", "gardener", "musician", "porter", "professor", "retired")
occup_stats = occup_stats %>% select(!all_of(occup_na))
occup_stats$occup_m = rowMeans(occup_stats[,2:39], na.rm = T)

write.csv(occup_stats, "occup_stats.csv")

d = d %>% select(!all_of(occup_na))
d$occup_m = rowMeans(d2[,2:39])

d$occup_m = rowMeans(d2[,2:47])
d$gss_m = d1$attitude

### mean ling gender bias 
### together
ggplot(data=d, aes(x=year)) +
  geom_line(aes(y = occup_m, color = "occup_m"))

### mean gender role attitude
ggplot(data=d, aes(x=year)) + 
  geom_line(aes(y = gss_m, color="gss_m"))

### together
ggplot(data=d, aes(x=year)) + 
  geom_line(aes(y = gss_m, color="gss_m")) +
  geom_line(aes(y = occup_m, color = "occup_m"))

res = ccf(d$occup_m, d$gss_m, lag = 10)

#ccf(d$teacher, d2$gss_m, lag = 10)
#ccf(d$soldier, d2$gss_m, lag = 10)

#ccf(d$police, d2$gss_m, lag = 10)
#ccf(d$doctor, d2$gss_m, lag = 10)

#ccf(d$dancer, d2$gss_m, lag = 10)
#ccf(d$engineer, d2$gss_m, lag = 10)
#ccf(d$nurse, d2$gss_m, lag = 10)

max_lags = c()
max_acfs = c()
filtered_occups = filtered_occups[!filtered_occups %in% occup_na]

for (occup in filtered_occups){
  res = ccf(d[,occup], d$gss_m, lag = 10, plot=F)
  res_df = do.call(rbind, Map(data.frame, lag=res$lag, acf=res$acf))
  max_lag = res_df$lag[which.max(res_df$acf)]
  max_acf = max(res_df$acf)
  max_lags = append(max_lags, max_lag)
  max_acfs = append(max_acfs, max_acf)
}
max_lags
mean(max_lags)

max_acfs
mean(max_acfs)

lag_df = do.call(rbind, Map(data.frame, occup=filtered_occups, max_lag=max_lags, max_acf=max_acfs))
write.csv(lag_df, "lag_df.csv")


max_lags_2 = c()
max_acfs_2 = c()

for (occup in filtered_occups){
  res = ccf(d[,occup], occup_stats[,occup], lag = 10, plot=F)
  res_df = do.call(rbind, Map(data.frame, lag=res$lag, acf=res$acf))
  max_lag = res_df$lag[which.max(res_df$acf)]
  max_acf = max(res_df$acf)
  max_lags_2 = append(max_lags_2, max_lag)
  max_acfs_2 = append(max_acfs_2, max_acf)
}
max_lags_2
mean(max_lags_2)

max_acfs_2
mean(max_acfs_2)

lag_df_2 = do.call(rbind, Map(data.frame, occup=filtered_occups, max_lag=max_lags_2, max_acf=max_acfs_2))
write.csv(lag_df, "lag_df_2.csv")

max_lags_3 = c()
max_acfs_3 = c()

for (occup in filtered_occups){
  res = ccf(occup_stats[,occup], d$gss_m, lag = 10, plot=F)
  res_df = do.call(rbind, Map(data.frame, lag=res$lag, acf=res$acf))
  max_lag = res_df$lag[which.max(res_df$acf)]
  max_acf = max(res_df$acf)
  max_lags_3 = append(max_lags_3, max_lag)
  max_acfs_3 = append(max_acfs_3, max_acf)
}
max_lags_3
mean(max_lags_3)

max_acfs_3
mean(max_acfs_3)

lag_df_3 = do.call(rbind, Map(data.frame, occup=filtered_occups, max_lag=max_lags_3, max_acf=max_acfs_3))
write.csv(lag_df, "lag_df_3.csv")

2/sqrt(18.5)

