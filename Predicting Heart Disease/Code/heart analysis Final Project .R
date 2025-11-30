# Load needed packages
library(tidyverse); library(caret); library(pROC); library(GGally)

# Read the dataset
df <- read.csv("heart.csv")

# Look at the data structure
glimpse(df)

# Convert required columns to factors
df <- df %>%
  mutate(
    sex = factor(sex),
    cp = factor(cp),
    fbs = factor(fbs),
    restecg = factor(restecg),
    exang = factor(exang),
    slope = factor(slope),
    thal = factor(thal),
    target = factor(target)
  )

# Check for missing values
colSums(is.na(df))

# Save a cleaned version
write.csv(df, "heart_clean.csv", row.names = FALSE)

# Basic summary of the dataset
summary(df)

# Plot: Age distribution by target
png("age_by_target.png", 800, 500)
ggplot(df, aes(age, fill = target)) + geom_histogram(bins = 20, position = "dodge")
dev.off()

# Plot: Cholesterol by target
png("chol_by_target.png", 800, 500)
ggplot(df, aes(target, chol, fill = target)) + geom_boxplot()
dev.off()

# Plot: Oldpeak by target
png("oldpeak_by_target.png", 800, 500)
ggplot(df, aes(target, oldpeak, fill = target)) + geom_boxplot()
dev.off()

# Pairplot for important numeric variables
png("pairplot_numeric.png", 1200, 900)
ggpairs(df[, c("age","trestbps","chol","thalach","oldpeak","target")], aes(color = target))
dev.off()

# Split the data into training and testing (80/20)
set.seed(123)
index <- createDataPartition(df$target, p = 0.8, list = FALSE)
train <- df[index, ]
test  <- df[-index, ]

# Build logistic regression model
logit_model <- glm(target ~ ., data = train, family = "binomial")

# Predict using logistic regression
test$logit_prob <- predict(logit_model, test, type = "response")
test$logit_pred <- ifelse(test$logit_prob > 0.5, "yes", "no")

# Confusion matrix for logistic regression
conf_logit <- confusionMatrix(factor(test$logit_pred), test$target)
conf_logit

# Logistic regression ROC curve
roc_logit <- roc(test$target, test$logit_prob)
png("roc_logistic.png", 700, 500)
plot(roc_logit)
dev.off()

# Train KNN with cross-validation
ctrl <- trainControl(method = "repeatedcv", number = 10, repeats = 3,
                     classProbs = TRUE, summaryFunction = twoClassSummary)

knn_model <- train(target ~ ., data = train, method = "knn",
                   trControl = ctrl, metric = "ROC",
                   preProcess = c("center","scale"),
                   tuneGrid = data.frame(k = seq(3, 31, 2)))

# Predict using KNN
test$knn_prob <- predict(knn_model, test, type = "prob")[, "yes"]
test$knn_pred <- predict(knn_model, test)

# Confusion matrix for KNN
conf_knn <- confusionMatrix(test$knn_pred, test$target)
conf_knn

# KNN ROC curve
roc_knn <- roc(test$target, test$knn_prob)
png("roc_knn.png", 700, 500)
plot(roc_knn)
dev.off()

# Compare both models
comparison <- data.frame(
  Model = c("Logistic Regression", "KNN"),
  Accuracy = c(conf_logit$overall["Accuracy"], conf_knn$overall["Accuracy"]),
  AUC = c(as.numeric(auc(roc_logit)), as.numeric(auc(roc_knn)))
)

# Save comparison table
write.csv(comparison, "model_comparison.csv", row.names = FALSE)

# Print comparison
comparison