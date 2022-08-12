# Military Operations Research Recipes
This repository collects relevant methods in the field of military operations research. It aims to approach the topics from the application side, while reducing the theoretical background to the bare minimum.  

## Optimal Search Strategy

This method is about optimizing search efforts in order to maximize the probabilty of detecting a potential opponent.
Considering the depicted situation below, it is self-evident that the propability of presence of enemy troops is nonuniform among the given areas A1 to A6.
If the opposing force has a strong marine and mechanized infantery, there is less chance of finding anything on a steep mountain side than on urban territory.

<p align="center"><img alt="interlaken regions" src="docs/img/regions_interlaken.png" width="70%"></p>

The presented method is a numerical recipe for finding the best possible search strategy.
In particular, it will determine, respectively optimizing, the search efforts in each area A1 to A6 in order to reach the highest accumulated probability of a search success.
The applied mathematical model is derived from the <b>random search formula of Koopman</b> and results in following optimization task: 

<p align="center"><img src="https://latex.codecogs.com/svg.image?P&space;=&space;\sum_{i=1}^{n}&space;p_i&space;(1&space;-&space;e^{-\frac{t_i}{T_i}})&space;\;\;\text{&space;where&space;}\;\;&space;T_i&space;=&space;\frac{A_i}{v&space;W}&space;&space;\;\;\text{&space;and&space;}\;\;&space;t&space;=&space;\sum_{i=1}^{n}&space;t_i,&space;t_i&space;\geq&space;0" title="P = \sum_{i=1}^{n} p_i (1 - e^{-\frac{t_i}{T_i}}) \;\;\text{ where }\;\; T_i = \frac{A_i}{v W} \;\;\text{ and }\;\; t = \sum_{i=1}^{n} t_i, t_i \geq 0" /></p>

Please note that <img src="https://latex.codecogs.com/svg.image?t_i" title="t_i" /> are the parameters to optimize and represent the search effort in time invested in the corresponding region, whereas <img src="https://latex.codecogs.com/svg.image?t" title="t" /> denotes the overall available search time.
The sensor parameters <img src="https://latex.codecogs.com/svg.image?W" title="W" /> is the <b>sweep width</b> and <img src="https://latex.codecogs.com/svg.image?v" title="W" /> the scanning speed.
<img src="https://latex.codecogs.com/svg.image?v" title="A_i" /> is a regions areal size and <img src="https://latex.codecogs.com/svg.image?v" title="p_i" /> the probability that a target might be located there. 
<img src="https://latex.codecogs.com/svg.image?P" title="P" /> is the overall probability of detection and core objective.  

Let's stick to above situation with the potential presence of tanks and battle ships.
The overall search effort is one day <img src="https://latex.codecogs.com/svg.image?t=24h"/>.
<img src="https://latex.codecogs.com/svg.image?i" title="i" /> | Type | <img src="https://latex.codecogs.com/svg.image?A_i&space;\;\;&space;[\text{km}^2]" title="A_i \;\; [\text{km}^2]" /> | <img src="https://latex.codecogs.com/svg.image?p_i" title="p_i" />  
--- | --- | --- | --- 
1 | urban | 14.1  | 0.6 
2 | mountain | 6.3  | 0.1 
3 | mountain | 4.1  | 0.1 
4 | water | 3.5  | 0.4 
5 | water | 1.9  | 0.4 
6 | mountain | 9.1  | 0.1

Reference: Military Operations Research, Jaiswal


