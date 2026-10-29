# Results

| Mode | GLEU vs gold |
|---|---|
| no change | 0.355 |
| pipeline (spell + model + safety) | 0.687 |
| model + safety (no spell) | 0.632 |
| model only | 0.664 |
| spell + model (no safety) | 0.708 |

## Example 1

**Input**

> i wnet there before and i has a apple.

**pipeline (spell + model + safety)**

> I went there before and I have an apple.

**model + safety (no spell)**

> I went there before and I have an apple.

**model only**

> I went there before and I have an apple.

**spell + model (no safety)**

> I went there before and I have an apple.

**Gold**

> I went there before, and I have an apple.

## Example 2

**Input**

> Because they were very hungry, they decided to cuuked a masive dinr on the sidewalk.

**pipeline (spell + model + safety)**

> Because they were very hungry, they decided to cook a massive diner on the sidewalk.

**model + safety (no spell)**

> Because they were very hungry, they decided to cuuked a massive diner on the sidewalk.

**model only**

> Because they were very hungry, they decided to pick a massive diner on the sidewalk.

**spell + model (no safety)**

> Because they were very hungry, they decided to cook a massive diner on the sidewalk.

**Gold**

> Because they were very hungry, they decided to cook a massive dinner on the sidewalk.

## Example 3

**Input**

> his there hosw your dasy today was it good to ahve you herer

**pipeline (spell + model + safety)**

> His there how your day today was it good to have you here .

**model + safety (no spell)**

> His there shout your dasy today was it good to have youherer

**model only**

> His there shout your dasy today was it good to have youherer

**spell + model (no safety)**

> His there how your day today was it good to have you here .

**Gold**

> Hi there, how was your day today? Was it good to have you here?

## Example 4

**Input**

> Yestrday, teh thry mans wos wenting to the grocry sohp for byuing sum fresh telvisions.

**pipeline (spell + model + safety)**

> Yesterday , the thy men were wanting to the grocery shop for buying sum fresh televisions.

**model + safety (no spell)**

> Today , the thy mans was going to the grocery shop for buying sum fresh televisions.

**model only**

> Today , the thy mans was going to the grocery shop for buying sum fresh televisions.

**spell + model (no safety)**

> Yesterday , the thy men were wanting to the grocery shop for buying sum fresh televisions.

**Gold**

> Yesterday, the three men were going to the grocery shop to buy some fresh televisions.

## Example 5

**Input**

> Yesturday, wen me an my freinds woz walken to the shoping center, we haz seen a veri big dog who barked lordly to we. Mi frend Jon, wich are normaly veri bravest, comed to runen awai bekaus he wer so much skared of the animles.

**pipeline (spell + model + safety)**

> Yesterday when I and my friends were walking to the shopping center , we seen a very big dog who barked lordly to us. My friend Jon, which is normal very bravest, comes to run away beaus he wears so much scared of the animes.

**model + safety (no spell)**

> Today when my friends were walking to the shopping center , we had seen a very big dog who barked kindly to us. My friend Jon, which is normaly very bravest, came to run away because he was so much skared of the animals.

**model only**

> Today when my friends were walking to the shopping center , we had seen a very big dog who barked kindly to us. My friend Jon, which is usually very bravest, came to run away because he was so much sacked of the animals.

**spell + model (no safety)**

> Yesterday when I and my friends were walking to the shopping center , we saw a very big dog who barked kindly to us. My friend Jon, which is normal very bravest, comes to run away beaus he wears so much scared of the animes.

**Gold**

> Yesterday, my friends and I walked to the shopping center. We saw a very big dog that barked loudly at us. My friend Jon, who is normally very brave, started to run away because he was so scared of the animal.

## Example 6

**Input**

> i dont no wat to do abot my homwork. its to hard four me.

**pipeline (spell + model + safety)**

> I don't know what to do about my homework. It is too hard for me.

**model + safety (no spell)**

> I don't know what to do about my work. It is too hard for me.

**model only**

> I don't know what to do about my work. It is too hard for me.

**spell + model (no safety)**

> I don't know what to do about my homework. It is too hard for me.

**Gold**

> I don't know what to do about my homework. It's too hard for me.

## Example 7

**Input**

> Last weak we goed to the beech and swimed all day. it was grate fun.

**pipeline (spell + model + safety)**

> Last weak we good to the beech and slime all day. It was grate fun.

**model + safety (no spell)**

> The last weak we went to the beech and swimed all day. It was grate fun.

**model only**

> The last weak we went to the beech and swimed all day. It was grate fun.

**spell + model (no safety)**

> Last weak we good to the beech and slime all day. It was grate fun.

**Gold**

> Last week we went to the beach and swam all day. It was great fun.

## Example 8

**Input**

> She dont like to eats vegetables, but she love fruits.

**pipeline (spell + model + safety)**

> She doesn't like to eat vegetables but she loves fruits.

**model + safety (no spell)**

> She does not like to eat vegetables but she loves fruits.

**model only**

> She does not like to eat vegetables but she loves fruits.

**spell + model (no safety)**

> She doesn't like to eat vegetables but she loves fruits.

**Gold**

> She doesn't like to eat vegetables, but she loves fruits.

## Example 9

**Input**

> My brother have two dog and a cat. They plays together every day.

**pipeline (spell + model + safety)**

> My brother have two dogs and a cat. They play together every day.

**model + safety (no spell)**

> My brother have two dogs and a cat. They play together every day.

**model only**

> My brother has two dogs and a cat. They play together every day.

**spell + model (no safety)**

> My brother has two dogs and a cat. They play together every day.

**Gold**

> My brother has two dogs and a cat. They play together every day.

## Example 10

**Input**

> Yesterday i buyed a new fone becuase my old one was broked.

**pipeline (spell + model + safety)**

> Yesterday I bayed a new one because my old one was broken.

**model + safety (no spell)**

> Yesterday I buyed a new fone because my old one was broken.

**model only**

> Yesterday I bought a new phone because my old one was broken.

**spell + model (no safety)**

> Yesterday I bought a new one because my old one was broken.

**Gold**

> Yesterday I bought a new phone because my old one was broken.

## Example 11

**Input**

> Their going to the libary to studdy for there exam tomorow.

**pipeline (spell + model + safety)**

> They are going to the library to study for their exam tomorrow.

**model + safety (no spell)**

> They are going to the library to study for their exam tomorrow.

**model only**

> They are going to the library to study for their exam tomorrow.

**spell + model (no safety)**

> They are going to the library to study for their exam tomorrow.

**Gold**

> They're going to the library to study for their exam tomorrow.

## Example 12

**Input**

> If i would have known about the meeting, i will come erly.

**pipeline (spell + model + safety)**

> If I would have known about the meeting , I will come early.

**model + safety (no spell)**

> If I would have known about the meeting , I will come again.

**model only**

> If I would have known about the meeting , I will come again.

**spell + model (no safety)**

> If I would have known about the meeting , I will come early.

**Gold**

> If I had known about the meeting, I would have come early.

## Example 13

**Input**

> The wheather is realy bad today, so we cant play outsid.

**pipeline (spell + model + safety)**

> The weather is really bad today, so we can't play outside.

**model + safety (no spell)**

> The weather is really bad today, so we can not play out.

**model only**

> The weather is really bad today, so we can not play out.

**spell + model (no safety)**

> The weather is really bad today, so we can't play outside.

**Gold**

> The weather is really bad today, so we can't play outside.

## Example 14

**Input**

> He asked me to borow him my bike, but i dident want to.

**pipeline (spell + model + safety)**

> He asked me to borrow him my bike, but I didn't want to.

**model + safety (no spell)**

> He asked me to borrow him my bike, but I did not want to.

**model only**

> He asked me to borrow him my bike, but I did not want to.

**spell + model (no safety)**

> He asked me to borrow him my bike, but I didn't want to.

**Gold**

> He asked me to lend him my bike, but I didn't want to.

## Example 15

**Input**

> We was very tired after the long jurney, so we goes to bed erly.

**pipeline (spell + model + safety)**

> We were very tired after the long journey, so we goes to bed early.

**model + safety (no spell)**

> We were very tired after the long jurney, so we goes to bed early.

**model only**

> We were very tired after the long lecture, so we went to bed early.

**spell + model (no safety)**

> We were very tired after the long journey, so we went to bed early.

**Gold**

> We were very tired after the long journey, so we went to bed early.

## Example 16

**Input**

> Can you give me a advice about which laptop i should to buy?

**pipeline (spell + model + safety)**

> Can you give me advice about which laptop I should buy?

**model + safety (no spell)**

> Can you give me advice about which laptop I should buy?

**model only**

> Can you give me advice about which laptop I should buy?

**spell + model (no safety)**

> Can you give me advice about which laptop I should buy?

**Gold**

> Can you give me some advice about which laptop I should buy?

## Example 17

**Input**

> The teacher explaned the lesson twise, but some studens still dident understand.

**pipeline (spell + model + safety)**

> The teacher explained the lesson wise, but some students still didn't understand.

**model + safety (no spell)**

> The teacher explained the lesson twise, but some students still dident understand.

**model only**

> The teacher explained the lesson right, but some students still dident understand.

**spell + model (no safety)**

> The teacher explained the lesson wise, but some students still didn't understand.

**Gold**

> The teacher explained the lesson twice, but some students still didn't understand.

## Example 18

**Input**

> Me and my sister was waiting for the bus when it begun to rain hardly.

**pipeline (spell + model + safety)**

> Me and my sister were waiting for the bus when it began to rain hardly.

**model + safety (no spell)**

> Me and my sister were waiting for the bus when it began to rain hardly.

**model only**

> Me and my sister were waiting for the bus when it began to rain hardly.

**spell + model (no safety)**

> Me and my sister were waiting for the bus when it began to rain hardly.

**Gold**

> My sister and I were waiting for the bus when it began to rain hard.

## Example 19

**Input**

> I have lived in this city since five years, and i realy like it.

**pipeline (spell + model + safety)**

> I have lived in this city since five years, and I really like it.

**model + safety (no spell)**

> I have lived in this city since five years, and I really like it.

**model only**

> I have lived in this city since five years, and I really like it.

**spell + model (no safety)**

> I have lived in this city since five years, and I really like it.

**Gold**

> I have lived in this city for five years, and I really like it.

## Example 20

**Input**

> Wen we arrived at the restorant, all the tabels was already taked.

**pipeline (spell + model + safety)**

> When we arrived at the restaurant, all the tables were already taken.

**model + safety (no spell)**

> When we arrived at the restorant, all the tables were already taken.

**model only**

> When we arrived at the restorant, all the tables were already taken.

**spell + model (no safety)**

> When we arrived at the restaurant, all the tables were already taken.

**Gold**

> When we arrived at the restaurant, all the tables were already taken.

## Example 21

**Input**

> She is more taller than her brother, but he is more stronger.

**pipeline (spell + model + safety)**

> She is more taller than her brother, but he is more stronger.

**model + safety (no spell)**

> She is more taller than her brother, but he is more stronger.

**model only**

> She is more taller than her brother, but he is more stronger.

**spell + model (no safety)**

> She is more taller than her brother, but he is more stronger.

**Gold**

> She is taller than her brother, but he is stronger.

## Example 22

**Input**

> Yesturday, my frend woz sik so he stayed at hom and sleeped all day.

**pipeline (spell + model + safety)**

> Yesterday, my friend was so he stayed at home and sleeved all day.

**model + safety (no spell)**

> Yesturday, my friend was sick so he stayed at home and sleeped all day.

**model only**

> Today, my friend was sick so he stayed at home and slept all day.

**spell + model (no safety)**

> Yesterday, my friend was so he stayed at home and sleeved all day.

**Gold**

> Yesterday, my friend was sick so he stayed at home and slept all day.

## Example 23

**Input**

> The childrens was playing in the garden whan it sudenly started to snow.

**pipeline (spell + model + safety)**

> The children were playing in the garden when it suddenly started to snow .

**model + safety (no spell)**

> The children were playing in the garden when it suddenly started to snow.

**model only**

> The children were playing in the garden when it suddenly started to snow.

**spell + model (no safety)**

> The children were playing in the garden when it suddenly started to snow .

**Gold**

> The children were playing in the garden when it suddenly started to snow.

## Example 24

**Input**

> I am agree with you, but i think we should to wait untill monday.

**pipeline (spell + model + safety)**

> I am agree with you, but I think we should wait until Monday.

**model + safety (no spell)**

> I am agree with you, but I think we should wait until Monday.

**model only**

> I am agree with you, but I think we should wait until Monday.

**spell + model (no safety)**

> I am agree with you, but I think we should wait until Monday.

**Gold**

> I agree with you, but I think we should wait until Monday.

## Example 25

**Input**

> Becouse of the traffic, we arrived late to the airport and misses our flight.

**pipeline (spell + model + safety)**

> Because of the traffic, we arrived late to the airport and missed our flight.

**model + safety (no spell)**

> Because of the traffic, we arrived late to the airport and missed our flight.

**model only**

> Because of the traffic, we arrived late to the airport and missed our flight.

**spell + model (no safety)**

> Because of the traffic, we arrived late to the airport and missed our flight.

**Gold**

> Because of the traffic, we arrived late at the airport and missed our flight.
