![title](assets/readmeimages/title.png)

Musical Theatre Quiz is a simple multiple choice quiz that offers the user a fun and exciting way of testing their knowledge of the musical arts. 
<br>
Get a question right? you get a point! Get a question wrong and it's all over! 
How many points can you get? Find out in [Musical Theatre Quiz](https://musical-theater-quiz-c67f89732c69.herokuapp.com/).

![mockup](assets/readmeimages/mockup.jpg)

# Contents
* [**User Experience**](<#user-experience>)
    * [User Stories](<#user-stories>)
    * [Wireframes](<#wireframes>)
    * [Flow Chart](<#flow-charts>)
    * [Design Choices](#design-choices)
        * [Typography](#typography)
        * [Colour Choices](#colour-choices)
* [**The Quiz**](<#the-quiz>)

# User Experience #

## User Stories ##
- As a user I would like an easy interface with clear instruction.
- As a user I would like the quiz to be difficult but fun.
- As a user I would like to be able to see the leaderboard. 
- As a user I would like to know my score and see how many points I can get.



## Wireframes ##
The initial wireframes were made on [Balsamiq](https://www.balsamiq.cloud). These wireframes of the quiz, show a somewhat less thought out design but shows how much I've built upon to make sure the UX is stronger.
<br>

![wireframes](assets/readmeimages/wireframes.png)

I wanted to make this a really easy interface with little distraction to ensure the user has the best experience. 

## Flow Charts ##
I made the flow chart using [Lucid Chart](https://www.lucidchart.com). This again shows a little more thought out process including different difficulties which would be offered in a future build. It also details how only 10 questions would be shown, I decided in terms of a competitive user experience, its better to have one mode and compete for that top spot. 

![lucidchart](assets/readmeimages/PP3.png)


## Design Choices ##

### Typograghy ###
Although technically not typography, the font art I used within my project was imported using [art](https://pypi.org/project/art/). I wanted the main screen to stand out and this can be seen by all headings within the quiz game. 

![font](assets/readmeimages/title.png)

### Colour Choices ###
The colours I've chosen were inspired by the french flag. Mainly because when thinking of a standout group of colours for musical theatre, the french flag is such a prominant option due to the musical Les Miserables and it helps the screen pop out too. So I used the Linear gradient on [Gradient CSS](http://www.gradientcss.com/) to help me achieve this. 

![Gradient backdrop](assets/readmeimages/gradientcss.png)

I also replicated this in the font colour choices for the most part of the quiz. 

# The Quiz #

## Main Page ##
the Quiz main screen is again inspired by the colours of the french flag (Les Miserables) and gives the user the option to enter their username, they can user characters and numbers. 
<br>

![Main Page](assets/readmeimages/welcomepage.png)

If the user enters a username that is less than 3 or more than 10 characters long, they will receive the following message;
![username error](assets/readmeimages/usernameerror.png)

Once they user has put in the correct username charachter count, they are welcomed by the main menu;

![Main menu](assets/readmeimages/mainmenu.png)

The user is then given 4 options.
- 1) [Play the Quiz](<#play-the-quiz>)
- 2) Instructions
- 3) Leaderboard
- 4) Exit Game

## Play the Quiz ##

When the user select option one, they will be pushed into the quiz.

![Quiz screen](assets/readmeimages/quizmain.png)

The user can then select 1,2,3 or 4 to choose their answer. If they guess correctly;

![Quiz screen](assets/readmeimages/correctanswer.png)

A point is added onto their tally and they continue onto the next question. 

If they guess incorrectly;

![Quiz screen](assets/readmeimages/incorrectanswer.png)

They are notified that they are incorrect, are supplied with the correct answer and then shown the game over screen;

![Quiz screen](assets/readmeimages/gameoverpage.png)

You only have oen life in this quiz. 

Furthermore, if the user gives an invalid option;

![Quiz screen](assets/readmeimages/quizmaininvalidoption.png)

If the user answers all 50 questions correctly (for the purposes of the readme, I reduced the amount of questions to 10); 
