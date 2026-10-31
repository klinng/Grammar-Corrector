# Results

| Mode | GLEU vs gold |
|---|---|
| no change | 0.518 |
| pipeline (spell + model + safety) | 0.870 |
| model + safety (no spell) | 0.777 |
| model only | 0.798 |
| spell + model (no safety) | 0.870 |

## Example 1

**Input**

> My sister is more smarter than me, but i am more faster then her.

**pipeline (spell + model + safety)**

> My sister is more smarter than me, but I am more faster than her.

**model + safety (no spell)**

> My sister is more smarter than me, but I am more faster than her.

**model only**

> My sister is more smarter than me, but I am more faster than her.

**spell + model (no safety)**

> My sister is more smarter than me, but I am more faster than her.

**Gold**

> My sister is smarter than me, but I am faster than her.

## Example 2

**Input**

> We are living in this house since ten years and we likes it.

**pipeline (spell + model + safety)**

> We are living in this house since ten years and we like it.

**model + safety (no spell)**

> We are living in this house since ten years and we like it.

**model only**

> We are living in this house since ten years and we like it.

**spell + model (no safety)**

> We are living in this house since ten years and we like it.

**Gold**

> We have lived in this house for ten years and we like it.

## Example 3

**Input**

> I am agree that the movie was to long, but the music was good.

**pipeline (spell + model + safety)**

> I am agree that the movie was too long, but the music was good.

**model + safety (no spell)**

> I am agree that the movie was too long, but the music was good.

**model only**

> I am agree that the movie was too long, but the music was good.

**spell + model (no safety)**

> I am agree that the movie was too long, but the music was good.

**Gold**

> I agree that the movie was too long, but the music was good.

## Example 4

**Input**

> He drive very carefull, so he never have a accident.

**pipeline (spell + model + safety)**

> He drives very carefully, so he never has an accident.

**model + safety (no spell)**

> He drives very carefully and never has an accident.

**model only**

> He drives very carefully and never has an accident.

**spell + model (no safety)**

> He drives very carefully, so he never has an accident.

**Gold**

> He drives very carefully, so he never has an accident.

## Example 5

**Input**

> If it will rain tomorow, we will stay at home.

**pipeline (spell + model + safety)**

> If it will rain tomorrow, we will stay at home.

**model + safety (no spell)**

> If it will rain tomorrow we will stay at home.

**model only**

> If it will rain tomorrow we will stay at home.

**spell + model (no safety)**

> If it will rain tomorrow, we will stay at home.

**Gold**

> If it rains tomorrow, we will stay at home.

## Example 6

**Input**

> The students was waiting for there teacher, but she dident come.

**pipeline (spell + model + safety)**

> The students were waiting for their teacher, but she didn't come.

**model + safety (no spell)**

> The students were waiting for their teacher, but she did not come.

**model only**

> The students were waiting for their teacher, but she did not come.

**spell + model (no safety)**

> The students were waiting for their teacher, but she didn't come.

**Gold**

> The students were waiting for their teacher, but she didn't come.

## Example 7

**Input**

> She sings beautifuly and plays the piano good.

**pipeline (spell + model + safety)**

> She sings beautifully and plays the piano well.

**model + safety (no spell)**

> She sings beautifully and plays the piano well.

**model only**

> She sings beautifully and plays the piano well.

**spell + model (no safety)**

> She sings beautifully and plays the piano well.

**Gold**

> She sings beautifully and plays the piano well.

## Example 8

**Input**

> Yesturday we visitted the museum, and the guide telled us many storys.

**pipeline (spell + model + safety)**

> Yesterday we visited the museum, and the guide told us many stories.

**model + safety (no spell)**

> Yesturday we visited the museum, and the guide telled us many stories.

**model only**

> Today we visited the museum, and the guide told us many stories.

**spell + model (no safety)**

> Yesterday we visited the museum, and the guide told us many stories.

**Gold**

> Yesterday we visited the museum, and the guide told us many stories.

## Example 9

**Input**

> I dont have no money, so i cant buy the tickit.

**pipeline (spell + model + safety)**

> I don't have any money, so I can't buy the ticket.

**model + safety (no spell)**

> I don't have any money, so I can't buy the tickit.

**model only**

> I don't have any money, so I can't buy the tickit.

**spell + model (no safety)**

> I don't have any money, so I can't buy the ticket.

**Gold**

> I don't have any money, so I can't buy the ticket.

## Example 10

**Input**

> Their are many peple in the park becuase the wheather is nice.

**pipeline (spell + model + safety)**

> There are many people in the park because the weather is nice.

**model + safety (no spell)**

> There are many people in the park because the wheather is nice.

**model only**

> There are many people in the park because the wheather is nice.

**spell + model (no safety)**

> There are many people in the park because the weather is nice.

**Gold**

> There are many people in the park because the weather is nice.

## Example 11

**Input**

> He suggested me to take a taxi, but i prefered to walk.

**pipeline (spell + model + safety)**

> He suggested me to take a taxi, but I preferred to walk.

**model + safety (no spell)**

> He suggested me to take a taxi, but I prefered to walk.

**model only**

> He suggested me to take a taxi, but I prefered to walk.

**spell + model (no safety)**

> He suggested me to take a taxi, but I preferred to walk.

**Gold**

> He suggested that I take a taxi, but I preferred to walk.

## Example 12

**Input**

> Every students must bring his book to the class.

**pipeline (spell + model + safety)**

> Every student must bring his book to the class.

**model + safety (no spell)**

> Every student must bring his book to the class.

**model only**

> Every student must bring his book to the class.

**spell + model (no safety)**

> Every student must bring his book to the class.

**Gold**

> Every student must bring his book to the class.

## Example 13

**Input**

> She has been working here since three months, and she is realy happy.

**pipeline (spell + model + safety)**

> She has been working here since three months, and she is really happy.

**model + safety (no spell)**

> She has been working here since three months, and she is really happy.

**model only**

> She has been working here since three months, and she is really happy.

**spell + model (no safety)**

> She has been working here since three months, and she is really happy.

**Gold**

> She has been working here for three months, and she is really happy.

## Example 14

**Input**

> The movie was so bored that we leaved before the end.

**pipeline (spell + model + safety)**

> The movie was so boring that we left before the end.

**model + safety (no spell)**

> The movie was so boring that we left before the end.

**model only**

> The movie was so boring that we left before the end.

**spell + model (no safety)**

> The movie was so boring that we left before the end.

**Gold**

> The movie was so boring that we left before the end.

## Example 15

**Input**

> My parents wants me to studying medicine, but i dont like it.

**pipeline (spell + model + safety)**

> My parents want me to study medicine, but I don't like it.

**model + safety (no spell)**

> My parents want me to study medicine, but I don't like it.

**model only**

> My parents want me to study medicine, but I don't like it.

**spell + model (no safety)**

> My parents want me to study medicine, but I don't like it.

**Gold**

> My parents want me to study medicine, but I don't like it.

## Example 16

**Input**

> Last night i seen a strange light in the sky and i was very scared.

**pipeline (spell + model + safety)**

> Last night I saw a strange light in the sky and I was very scared.

**model + safety (no spell)**

> Last night I saw a strange light in the sky and I was very scared.

**model only**

> Last night I saw a strange light in the sky and I was very scared.

**spell + model (no safety)**

> Last night I saw a strange light in the sky and I was very scared.

**Gold**

> Last night I saw a strange light in the sky and I was very scared.

## Example 17

**Input**

> He is the most tallest boy in our class, and he play basketball.

**pipeline (spell + model + safety)**

> He is the most tallest boy in our class, and he plays basketball.

**model + safety (no spell)**

> He is the most tallest boy in our class, and he plays basketball.

**model only**

> He is the most tallest boy in our class, and he plays basketball.

**spell + model (no safety)**

> He is the most tallest boy in our class, and he plays basketball.

**Gold**

> He is the tallest boy in our class, and he plays basketball.

## Example 18

**Input**

> I look forward to see you at the party next weak.

**pipeline (spell + model + safety)**

> I look forward to seeing you at the party next weak.

**model + safety (no spell)**

> I look forward to seeing you at the party next weak.

**model only**

> I look forward to seeing you at the party next weak.

**spell + model (no safety)**

> I look forward to seeing you at the party next weak.

**Gold**

> I look forward to seeing you at the party next week.

## Example 19

**Input**

> Because of the rain, the match was cancelled and everyone goed home sad.

**pipeline (spell + model + safety)**

> Because of the rain, the match was cancelled and everyone went home sad.

**model + safety (no spell)**

> Because of the rain, the match was cancelled and everyone goed home sad.

**model only**

> Because of the rain, the match was cancelled and everyone went home sad.

**spell + model (no safety)**

> Because of the rain, the match was cancelled and everyone went home sad.

**Gold**

> Because of the rain, the match was cancelled and everyone went home sad.

## Example 20

**Input**

> She asked me where was the station, but i dont knew.

**pipeline (spell + model + safety)**

> She asked me where was the station, but I don't know.

**model + safety (no spell)**

> She asked me where was the station, but I did not know.

**model only**

> She asked me where was the station, but I did not know.

**spell + model (no safety)**

> She asked me where was the station, but I don't know.

**Gold**

> She asked me where the station was, but I didn't know.
