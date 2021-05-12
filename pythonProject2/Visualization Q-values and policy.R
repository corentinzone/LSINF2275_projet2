#***************************************************************************************#
#               LSINF2275 - Data mining & Decision Making                               #
#                       Project 2: BlackJack                                            #
#                                                                                       #
#   Authors :   BAILLY Gabriel                                                          #
#               WAUTIER Lara                                                            #
#               ZONE Corentin                                                           #
#   Program :   DATS2M                                                                  #
#                                                                                       #
#   inspiration: https://www.askpython.com/python/examples/blackjack-game-using-python  #
#                                                                                       #
#***************************************************************************************#

library(ggplot2)
library(rayshader)
library(tidyverse)
library(patchwork)
setwd("~/DATS1M/Q2/SINF2275 - Data mining and decision making/Second Project/LSINF2275_projet2/pythonProject2") # change if needed


# --- Visualise Q-value function --- #

### if 'usable ace = True'

Qtrue = read.csv("Q-values true.csv", header=T)[,-1]
rownames(Qtrue) = c(4:21)
colnames(Qtrue) = c(1:10)

dealer = rep(1:10, 18)
player = c(rep(4,10), rep(5,10), rep(6,10), rep(7,10), rep(8, 10), rep(9,10),
           rep(10,10), rep(11,10), rep(12,10), rep(13,10), rep(14,10), rep(15,10),
           rep(16,10), rep(17,10), rep(18, 10), rep(19, 10), rep(20, 10), rep(21, 10))
qvalue = rep(0,180)
for (i in 1:18){
  for (j in 1:10){
    qvalue[(i-1)*10+j] = Qtrue[i,j]
  }
}

Qtrue = as.data.frame(cbind(player, dealer, qvalue))

mtplot_density = ggplot(Qtrue[81:180,]) + theme_bw() +
  aes(x=dealer,y=player, fill=qvalue) +
  geom_tile() + 
  scale_x_discrete(limits=1:10) +
  scale_y_discrete(limits=12:21) +
  scale_fill_gradient(low="pink", high="red")
mtplot_density

plot_gg(mtplot_density, multicore = TRUE, width = 8, height = 7, scale = 300, 
        background = "#afceff",shadowcolor = "#3a4f70",windowsize=c(1400,866),
        zoom = 0.55, phi = 30)
render_snapshot()
render_movie("Q-values (ace=True).mp4")

### if 'usable ace = True'

Qfalse = read.csv("Q-values false.csv", header=T)[,-1]
rownames(Qfalse) = c(4:21)
colnames(Qfalse) = c(1:10)
qvalueFalse = rep(0,180)
for (i in 1:18){
  for (j in 1:10){
    qvalueFalse[(i-1)*10+j] = Qfalse[i,j]
  }
}
Qfalse = as.data.frame(cbind(player, dealer, qvalueFalse))

mtplot_density2 = ggplot(Qfalse[81:180,]) + theme_bw() +
  aes(x=dealer,y=player, fill=qvalueFalse) +
  geom_tile() + 
  scale_x_discrete(limits=1:10) +
  scale_y_discrete(limits=12:21) +
  scale_fill_gradient(low="pink", high="red") + 
  labs(fill = "qvalue") 
mtplot_density2

#-------------------------------------------------------------------------------

# --- Visualise policy --- #

### if 'usable ace = True'

polTrue = as.numeric(read.csv("policy true.csv", header=T)[,3])
pTrue = as.data.frame(cbind(player, dealer, polTrue))
policyPlot = ggplot(pTrue[81:180,]) + theme_bw() +
  aes(x=dealer,y=player, fill=as.factor(polTrue)) +
  geom_tile() + 
  scale_x_discrete(limits=1:10) +
  scale_y_discrete(limits=12:21) +
  scale_fill_manual(values = c("#FAE0F1", "red"), labels = c("Stick", "Hit")) + 
  labs(fill = "Action") 

### if 'usable ace = False'

polFalse = as.numeric(read.csv("policy false.csv", header=T)[,3])
pFalse = as.data.frame(cbind(player, dealer, polFalse))
policyPlot2 = ggplot(pFalse[81:180,]) + theme_bw() +
  aes(x=dealer, y=player, fill=as.factor(polFalse)) +
  geom_tile() + 
  scale_x_discrete(limits=1:10) +
  scale_y_discrete(limits=12:21) +
  scale_fill_manual(values = c("#FAE0F1", "red"), labels = c("Stick", "Hit")) + 
  labs(fill = "Action") 

# --- Plot print zone --- #

# PLOT TRUE :

mtplot_density + policyPlot

# PLOT FALSE :

mtplot_density2 + policyPlot2

# TOTAL :

(mtplot_density + policyPlot) / (mtplot_density2 + policyPlot2) + 
  plot_annotation(title = 'Q-value function and policy',
                  subtitle = 'First row : usable ace = True, Second row : usable ace = False')

# Q-value TRUE vs. FALSE boxplot
qv = c(qvalue, qvalueFalse)
aceUsable = factor(c(rep("True", 180), rep("False", 180)), levels = c("True", "False"))
dftemp = as.data.frame(cbind(qv, aceUsable))
ggplot(dftemp) +
  theme_bw() +
  geom_boxplot(aes(y = qv, x = aceUsable, group = aceUsable), fill = "lightblue") +
  scale_x_continuous(breaks = c(1,2), labels = c("True", "False")) +
  labs(title = "Boxplot of Q-values",
       subtitle = "Difference of distribution when usable ace or not") +
  xlab("Usable Ace") +
  ylab("Q-Values")

# visualize win rate
library(forecast)
winrate = ts(read.csv("win rate.csv", header=T)[,2])
autoplot(winrate, main = "Percentage of winnings (1000 simulations)") + theme_bw() +
  xlab("Number of simulations") +
  ylab("Win Rate") +
  geom_hline(yintercept = mean(winrate[200:1000]), linetype = "dashed", color = "blue")