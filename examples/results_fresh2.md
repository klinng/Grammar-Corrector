# Results

| Mode | GLEU vs gold |
|---|---|
| no change | 0.620 |
| pipeline (spell + model + safety) | 0.794 |
| model + safety (no spell) | 0.754 |
| model only | 0.765 |
| spell + model (no safety) | 0.794 |

## Example 1

**Input**

> My cousin is more older than me, and he is more richer than my uncle.

**pipeline (spell + model + safety)**

> My cousin is more older than me, and he is more richer than my uncle.

**model + safety (no spell)**

> My cousin is more older than me, and he is more richer than my uncle.

**model only**

> My cousin is more older than me, and he is more richer than my uncle.

**spell + model (no safety)**

> My cousin is more older than me, and he is more richer than my uncle.

**Gold**

> My cousin is older than me, and he is richer than my uncle.

## Example 2

**Input**

> They are waiting for the bus since two hours, and the weather is cold.

**pipeline (spell + model + safety)**

> They are waiting for the bus since two hours, and the weather is cold.

**model + safety (no spell)**

> They are waiting for the bus since two hours, and the weather is cold.

**model only**

> They are waiting for the bus since two hours, and the weather is cold.

**spell + model (no safety)**

> They are waiting for the bus since two hours, and the weather is cold.

**Gold**

> They have been waiting for the bus for two hours, and the weather is cold.

## Example 3

**Input**

> I am disagree with the manager about the new schedule.

**pipeline (spell + model + safety)**

> I am disagree with the manager about the new schedule.

**model + safety (no spell)**

> I am disagree with the manager about the new schedule.

**model only**

> I am disagree with the manager about the new schedule.

**spell + model (no safety)**

> I am disagree with the manager about the new schedule.

**Gold**

> I disagree with the manager about the new schedule.

## Example 4

**Input**

> If the manager will agree, we will start the project on monday.

**pipeline (spell + model + safety)**

> If the manager will agree, we will start the project on Monday.

**model + safety (no spell)**

> If the manager will agree, we will start the project on Monday.

**model only**

> If the manager will agree, we will start the project on Monday.

**spell + model (no safety)**

> If the manager will agree, we will start the project on Monday.

**Gold**

> If the manager agrees, we will start the project on Monday.

## Example 5

**Input**

> The doctor recommended me to drink more water and to sleep early.

**pipeline (spell + model + safety)**

> The doctor recommended me to drink more water and to sleep early.

**model + safety (no spell)**

> The doctor recommended me to drink more water and to sleep early.

**model only**

> The doctor recommended me to drink more water and to sleep early.

**spell + model (no safety)**

> The doctor recommended me to drink more water and to sleep early.

**Gold**

> The doctor recommended that I drink more water and sleep early.

## Example 6

**Input**

> He wondered why was the shop closed so erly.

**pipeline (spell + model + safety)**

> He wondered why the shop closed so early.

**model + safety (no spell)**

> He wondered why was the shop closed so early.

**model only**

> He wondered why was the shop closed so early.

**spell + model (no safety)**

> He wondered why the shop closed so early.

**Gold**

> He wondered why the shop was closed so early.

## Example 7

**Input**

> Next weak my family is going to visit us from Canada.

**pipeline (spell + model + safety)**

> Next weak my family is going to visit us from Canada.

**model + safety (no spell)**

> Next weak my family is going to visit us from Canada.

**model only**

> Next weak my family is going to visit us from Canada.

**spell + model (no safety)**

> Next weak my family is going to visit us from Canada.

**Gold**

> Next week my family is going to visit us from Canada.

## Example 8

**Input**

> Yesterday the childrens played football and breaked a window.

**pipeline (spell + model + safety)**

> Yesterday the children played football and broke a window.

**model + safety (no spell)**

> Yesterday the children played football and breaked a window.

**model only**

> Yesterday the children played football and broke a window.

**spell + model (no safety)**

> Yesterday the children played football and broke a window.

**Gold**

> Yesterday the children played football and broke a window.

## Example 9

**Input**

> She dont understand why her brother is allways angry.

**pipeline (spell + model + safety)**

> She doesn't understand why her brother is always angry.

**model + safety (no spell)**

> She does not understand why her brother is always angry.

**model only**

> She does not understand why her brother is always angry.

**spell + model (no safety)**

> She doesn't understand why her brother is always angry.

**Gold**

> She doesn't understand why her brother is always angry.

## Example 10

**Input**

> We was very hungry, so we ordered two pizzas and eated them all.

**pipeline (spell + model + safety)**

> We were very hungry, so we ordered two pizzas and eaten them all.

**model + safety (no spell)**

> We were very hungry, so we ordered two pizzas and eated them all.

**model only**

> We were very hungry, so we ordered two pizzas and enjoyed them all.

**spell + model (no safety)**

> We were very hungry, so we ordered two pizzas and eaten them all.

**Gold**

> We were very hungry, so we ordered two pizzas and ate them all.

## Example 11

**Input**

> The new restaurant is the most cheapest in the whole town.

**pipeline (spell + model + safety)**

> The new restaurant is the most cheapest in the whole town.

**model + safety (no spell)**

> The new restaurant is the most cheapest in the whole town.

**model only**

> The new restaurant is the most cheapest in the whole town.

**spell + model (no safety)**

> The new restaurant is the most cheapest in the whole town.

**Gold**

> The new restaurant is the cheapest in the whole town.

## Example 12

**Input**

> My friend has been living in Spain since six years, and he speak spanish fluently.

**pipeline (spell + model + safety)**

> My friend has been living in Spain since six years, and he speaks spanish fluently.

**model + safety (no spell)**

> My friend has been living in Spain since six years, and he speaks spanish fluently.

**model only**

> My friend has been living in Spain since six years, and he speaks spanish fluently.

**spell + model (no safety)**

> My friend has been living in Spain since six years, and he speaks spanish fluently.

**Gold**

> My friend has been living in Spain for six years, and he speaks Spanish fluently.

## Example 13

**Input**

> I could not hear him becuase the music was to loud.

**pipeline (spell + model + safety)**

> I could not hear him because the music was too loud.

**model + safety (no spell)**

> I could not hear him because the music was too loud.

**model only**

> I could not hear him because the music was too loud.

**spell + model (no safety)**

> I could not hear him because the music was too loud.

**Gold**

> I could not hear him because the music was too loud.

## Example 14

**Input**

> If you will come early, i can show you the garden.

**pipeline (spell + model + safety)**

> If you will come early,, I can show you the garden.

**model + safety (no spell)**

> If you will come early,, I can show you the garden.

**model only**

> If you will come early,, I can show you the garden.

**spell + model (no safety)**

> If you will come early,, I can show you the garden.

**Gold**

> If you come early, I can show you the garden.

## Example 15

**Input**

> Nobody know where is the key to the garage.

**pipeline (spell + model + safety)**

> Nobody knows where is the key to the garage.

**model + safety (no spell)**

> Nobody knows where is the key to the garage.

**model only**

> Nobody knows where is the key to the garage.

**spell + model (no safety)**

> Nobody knows where is the key to the garage.

**Gold**

> Nobody knows where the key to the garage is.

## Example 16

**Input**

> The teacher suggested us to read two books during the holidays.

**pipeline (spell + model + safety)**

> The teacher suggested us to read two books during the holidays.

**model + safety (no spell)**

> The teacher suggested us to read two books during the holidays.

**model only**

> The teacher suggested us to read two books during the holidays.

**spell + model (no safety)**

> The teacher suggested us to read two books during the holidays.

**Gold**

> The teacher suggested that we read two books during the holidays.

## Example 17

**Input**

> Their was a big accident on the highway, and many cars was damaged.

**pipeline (spell + model + safety)**

> There was a big accident on the highway, and many cars were damaged.

**model + safety (no spell)**

> There was a big accident on the highway, and many cars were damaged.

**model only**

> There was a big accident on the highway, and many cars were damaged.

**spell + model (no safety)**

> There was a big accident on the highway, and many cars were damaged.

**Gold**

> There was a big accident on the highway, and many cars were damaged.

## Example 18

**Input**

> I have forgot my umbrela at the office, so i got wet.

**pipeline (spell + model + safety)**

> I have forgot my umbrella at the office, so I got wet.

**model + safety (no spell)**

> I have forgot my umbrella at the office, so I got wet.

**model only**

> I have forgot my umbrella at the office, so I got wet.

**spell + model (no safety)**

> I have forgot my umbrella at the office, so I got wet.

**Gold**

> I forgot my umbrella at the office, so I got wet.

## Example 19

**Input**

> He is more intelligent then his classmates, but he dont study hard.

**pipeline (spell + model + safety)**

> He is more intelligent than his classmates, but he doesn't study hard.

**model + safety (no spell)**

> He is more intelligent than his classmates, but he does not study hard.

**model only**

> He is more intelligent than his classmates, but he does not study hard.

**spell + model (no safety)**

> He is more intelligent than his classmates, but he doesn't study hard.

**Gold**

> He is more intelligent than his classmates, but he doesn't study hard.

## Example 20

**Input**

> We should of left earlier, becouse the train was already gone.

**pipeline (spell + model + safety)**

> We should have left earlier, because the train was already gone.

**model + safety (no spell)**

> We should have left earlier, because the train was already gone.

**model only**

> We should have left earlier, because the train was already gone.

**spell + model (no safety)**

> We should have left earlier, because the train was already gone.

**Gold**

> We should have left earlier, because the train was already gone.
