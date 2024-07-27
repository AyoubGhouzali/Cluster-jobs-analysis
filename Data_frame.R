library(RMySQL)
library(dplyr)
library(lubridate)

#connection_DB
HPC_DB <- dbConnect(MySQL(), user="root", db= "hpc-marwan", host="localhost")
allTables <- dbListTables(HPC_DB)

#Importer les données sur le cluster
Jobs23=read.table("C:/Users/ayoub/Desktop/Stage 1A/Raw data/JOBS_2023.csv", sep="|", header=TRUE)

Jobs24=read.table("C:/Users/ayoub/Desktop/Stage 1A/Raw data/JOBS_2024.csv", sep="|", header=TRUE)

#combiner des deux data frames et éviter les doublons
merged_Jobs <- rbind(Jobs23, Jobs24)
Jobs <- distinct(merged_Jobs)

Jobs$Submit <-ymd_hms(Jobs$Submit)
Jobs$Start <-ymd_hms(Jobs$Start)
Jobs<- Jobs %>% mutate(Year = year(Jobs$Submit), Month = month(Jobs$Submit))

write.csv(Jobs, file = "C:/Users/ayoub/Desktop/Stage 1A/Data frames/Jobs.csv")

#les jobs avec etablissement, domaine et université
Jobs_univ <- select(Jobs, JobID, JobName, UID, User, Partition,Account, Submit, Start, NCPUS, NNodes, State, Year, Month)


#Lire les tables de la base de données
hpc_utilisateur <- dbReadTable(HPC_DB, "hpc_utilisateur")
hpc_utilisateur <- select(hpc_utilisateur, id_utilisateur, etab_id_etablissement, dom_id_domaine)
hpc_universite <- dbReadTable(HPC_DB, "hpc_universite")
hpc_etablissement <- dbReadTable(HPC_DB, "hpc_etablissement")
hpc_domaine <- dbReadTable(HPC_DB, "hpc_domaine")
hpc_etablissement <- select(hpc_etablissement, id_etablissement, univ_id_universite)


names(hpc_utilisateur)[2] <- "id_etablissement"

result <- inner_join(hpc_utilisateur, hpc_etablissement, by = "id_etablissement")
names(result)[4] <- "id_universite"
result<- inner_join(result, hpc_universite, by = "id_universite")
result <- select(result, 1:6)
names(result)[3] <- "id_domaine"
result <- left_join(result, hpc_domaine, by = "id_domaine")

names(Jobs_univ)[3] <- "id_utilisateur"
Jobs_univ <- inner_join(Jobs_univ, result, by = "id_utilisateur")

write.csv(Jobs_univ, file = "C:/Users/ayoub/Desktop/Stage 1A/Data frames/Jobs_univ.csv")

#Le temps d'attente des jobs finis
waittime<- select(Jobs,NCPUS, Partition, State, Year,7:8)
waittime<- waittime %>% filter(State=="COMPLETED")
waittime<- waittime %>%mutate(Attente=Start-Submit)
waittime$NCPUS <- as.numeric(waittime$NCPUS)
waittime$Partition <- as.factor(waittime$Partition)
waittime$Attente_numeric <- as.numeric(waittime$Attente, units = "secs")
waittime <- waittime %>% mutate(ncpus_category = case_when(
  NCPUS == 0 ~ "0",
  NCPUS >= 1 & NCPUS <= 7 ~ "1-7",
  NCPUS >= 8 & NCPUS <= 15 ~ "8-15",
  NCPUS >= 16 & NCPUS <= 31 ~ "16-31",
  NCPUS >= 32 & NCPUS <= 64 ~ "32-64",
  TRUE ~ "PLUS"))

write.csv(waittime, "C:/Users/ayoub/Desktop/Stage 1A/Data frames/waittime.csv")

#boxplots for each year
waittime22 <- waittime %>% filter(Year == 2022)
waittime23 <- waittime %>% filter(Year == 2023)
waittime24 <- waittime %>% filter(Year == 2024)


#summary by partition
summary_stats_par22 <- waittime22 %>%
  group_by(Partition) %>%
  summarise(
    Min = min(Attente_numeric),
    `1st_Qu.` = quantile(Attente_numeric, 0.25),
    Median = median(Attente_numeric),
    Mean = mean(Attente_numeric),
    `3rd_Qu.` = quantile(Attente_numeric, 0.75),
    Max = max(Attente_numeric)
  )

summary_stats_par23 <- waittime23 %>%
  group_by(Partition) %>%
  summarise(
    Min = min(Attente_numeric),
    `1st_Qu.` = quantile(Attente_numeric, 0.25),
    Median = median(Attente_numeric),
    Mean = mean(Attente_numeric),
    `3rd_Qu.` = quantile(Attente_numeric, 0.75),
    Max = max(Attente_numeric)
  )

summary_stats_par24 <- waittime24 %>%
  group_by(Partition) %>%
  summarise(
    Min = min(Attente_numeric),
    `1st_Qu.` = quantile(Attente_numeric, 0.25),
    Median = median(Attente_numeric),
    Mean = mean(Attente_numeric),
    `3rd_Qu.` = quantile(Attente_numeric, 0.75),
    Max = max(Attente_numeric)
  )

#merge summary by partition
summary_stats_par22$Year <- 2022
summary_stats_par23$Year <- 2023
summary_stats_par24$Year <- 2024

waittime_stats_par<- rbind(summary_stats_par22, summary_stats_par23, summary_stats_par24)
waittime_stats_par$Year <- factor(waittime_stats_par$Year)
write.csv(waittime_stats_par, "C:/Users/ayoub/Desktop/Stage 1A/Data frames/waittime_boxp_par.csv")




#summary by ncpus
summary_stats_ncpus22 <- waittime22 %>%
  group_by(ncpus_category) %>%
  summarise(
    Min = min(Attente_numeric),
    `1st_Qu.` = quantile(Attente_numeric, 0.25),
    Median = median(Attente_numeric),
    Mean = mean(Attente_numeric),
    `3rd_Qu.` = quantile(Attente_numeric, 0.75),
    Max = max(Attente_numeric)
  )

summary_stats_ncpus23 <- waittime23 %>%
  group_by(ncpus_category) %>%
  summarise(
    Min = min(Attente_numeric),
    `1st_Qu.` = quantile(Attente_numeric, 0.25),
    Median = median(Attente_numeric),
    Mean = mean(Attente_numeric),
    `3rd_Qu.` = quantile(Attente_numeric, 0.75),
    Max = max(Attente_numeric)
  )

summary_stats_ncpus24 <- waittime24 %>%
  group_by(ncpus_category) %>%
  summarise(
    Min = min(Attente_numeric),
    `1st_Qu.` = quantile(Attente_numeric, 0.25),
    Median = median(Attente_numeric),
    Mean = mean(Attente_numeric),
    `3rd_Qu.` = quantile(Attente_numeric, 0.75),
    Max = max(Attente_numeric)
  )

#Merge summary by ncpus
summary_stats_ncpus22$Year <- 2022
summary_stats_ncpus23$Year <- 2023
summary_stats_ncpus24$Year <- 2024
waittime_stats_ncpus<- rbind(summary_stats_ncpus22, summary_stats_ncpus23, summary_stats_ncpus24)
waittime_stats_ncpus$Year <- factor(waittime_stats_ncpus$Year)
waittime_stats_ncpus$ncpus_category <- factor(waittime_stats_ncpus$ncpus_category, levels = c("0","1-7","8-15","16-31","32-64","PLUS"))
write.csv(waittime_stats_ncpus, "C:/Users/ayoub/Desktop/Stage 1A/Data frames/waittime_boxp_ncpus.csv")
