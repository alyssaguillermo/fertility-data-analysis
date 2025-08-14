install.packages("ggplot2")
library(ggplot2)

# set column names
columns <- c(
  "Season", 
  "Age", 
  "ChildishDisease", 
  "Accident", 
  "Surgery", 
  "HighFevers", 
  "AlcoholConsumptionFrequency", 
  "SmokingHabit", 
  "SittingHoursinDay", 
  "Diagnosis"
)

# read txt file 
data <- read.csv("/Users/alyssaguillermo/Downloads/python projects/fertility/fertility-data-analysis/fertility_Diagnosis.txt",
                 header = TRUE,
                 col.names = columns
                 )

# convert normalized age (0–1) to real age (18–36)
data$Age <- round(data$Age * (36 - 18) + 18)

# dictionaries to convert numerical values to strings
season_map <- c("-1"="Winter", "-0.33"="Spring", "0.33"="Summer", "1"="Fall")
child_map <- c("0"="Yes", "1"="No")
acc_map <- c("0"="Yes", "1"="No")
surg_map <- c("0"="Yes", "1"="No")
fever_map <- c("-1"="< 3 months ago", "0"="> 3 months ago", "1"="No")
smoke_map <- c("-1"="Never", "0"="Occasionally", "1"="Daily")
diag_map <- c("N"="Normal", "O"="Altered")
alcohol_map <- c(
  "0.2"="Several times a day",
  "0.4"="Every day",
  "0.6"="Several times a week",
  "0.8"="Once a week",
  "1"="Hardly ever/Never"
)

# convert normalized sitting hours (0-1) to real sitting hours (0-16)
data$'SittingHoursinDay' <- round(
  data$'SittingHoursinDay' * (16 - 0) + 0
)

# apply dictionary conversions
data$Season <- season_map[as.character(data$Season)]
data$`ChildishDisease` <- child_map[as.character(data$`ChildishDisease`)]
data$`Accident` <- acc_map[as.character(data$`Accident`)]
data$`Surgery` <- surg_map[as.character(data$`Surgery`)]
data$`HighFevers` <- fever_map[as.character(data$`HighFevers`)]
data$`SmokingHabit` <- smoke_map[as.character(data$`SmokingHabit`)]
data$`Diagnosis` <- diag_map[as.character(data$`Diagnosis`)]

# alcohol mapping (round)
data$`AlcoholConsumptionFrequency` <- round(data$`AlcoholConsumptionFrequency`, 2)
data$`AlcoholConsumptionFrequency` <- alcohol_map[as.character(data$`AlcoholConsumptionFrequency`)]

# custom order of x-axis bars
custom_order <- c(
  "Hardly ever/Never",
  "Once a week",
  "Several times a week",
  "Every day",
  "Several times a day"
)
data$`AlcoholConsumptionFrequency` <- factor(
  data$`AlcoholConsumptionFrequency`,
  levels = custom_order
)

# count occurrences in custom order
count_data <- as.data.frame(table(
  Alcohol = data$`AlcoholConsumptionFrequency`,
  Diagnosis = data$Diagnosis
))

# plot bars
ggplot(count_data, aes(x = Alcohol, y = Freq, fill = Diagnosis)) +
  geom_bar(stat = "identity", position = position_dodge()) +
  scale_fill_manual(values = c("Normal" = "skyblue", "Altered" = "salmon")) +
  labs(
    title = "Alcohol Consumption by Diagnosis",
    x = "Alcohol Consumption Frequency",
    y = "Count"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1))