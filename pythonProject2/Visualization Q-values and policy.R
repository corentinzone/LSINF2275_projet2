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
  scale_x_continuous(expand=c(0,0)) +
  scale_y_continuous(expand=c(0,0)) +
  scale_fill_gradient(low="pink", high="red")
mtplot_density

plot_gg(mtplot_density, multicore = TRUE, width = 8, height = 7, scale = 300, 
        background = "#afceff",shadowcolor = "#3a4f70",windowsize=c(1400,866),
        zoom = 0.55, phi = 30)
render_movie("Q-values (ace=True).mp4")



polTrue = as.numeric(read.csv("policy true.csv", header=T)[,3])
pTrue = as.data.frame(cbind(player, dealer, polTrue))
ggplot(pTrue[81:180,]) + theme_bw() +
  aes(x=dealer,y=player, fill=polTrue) +
  geom_tile() +
  scale_x_continuous(expand=c(0,0)) +
  scale_y_continuous(expand=c(0,0)) +
  scale_fill_gradient(low="white", high="red")


