# Military Operations Research Recipes
This repository collects relevant methods in the field of military operations research. It aims to approach the topics from the application side, while reducing the theoretical background to the bare minimum.  

## Optimal Search Strategy

This method is about optimizing search efforts in order to maximize the probabilty of detecting a potential opponent.
Considering the depicted situation below, it is self-evident that the propability of presence of enemy troops is nonuniform among the given areas A1 to A6.
If the opposing force has a strong marine and mechanized infantery, there is less chance of finding anything on a steep mountain side.

<p align="center"><img alt="interlaken regions" src="docs/img/regions_interlaken.png" width="70%"></p>

<p align="center"><img src="https://latex.codecogs.com/png.image?\dpi{150}&space;\bg_white&space;P&space;=&space;\sum_{i=1}^{n}&space;p_i&space;(1&space;-&space;e^{-\frac{t_i}{T_i}})&space;\;\;\text{&space;&space;where&space;&space;}\;\;&space;T_i&space;=&space;\frac{A_i}{v_i&space;W_i}" title="\bg_white P = \sum_{i=1}^{n} p_i (1 - e^{-\frac{t_i}{T_i}}) \;\;\text{ where }\;\; T_i = \frac{A_i}{v_i W_i}" /></p>

Reference: Military Operations Research, Jaiswal


