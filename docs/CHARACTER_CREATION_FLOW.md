## Character Creation Flow

The character creation process will begin after the player enters from the main screen using the (C)reate
character option. A new interface will be displayed containing a character sheet with blank attributes and an empty portrait placeholder. The flow of data entry will appear as follows:

- Choose gender (from (M)ale, (F)emale, or (O)ther).
- Choose Race (from the races.json file)
- Choose Subrace (from the subraces of the chosen race)
- Choose Class (from the classes.json file)
- Choose Subclass (from the subclasses of the chosen class)
- Roll for stats (base random number for each stat + race/subrace modifiers as well as class minimums)
- Bonus roll for points to distribute/customize their attributes further
- Add/Modify skills (some skills will be innate based on race/subrace/class/subclass). Classes and races
  will determine what available skills a character can choose from. We will need to determine a starting number of skill points that can be distributed.
- Choose a portrait. At this stage, there are no portraits but assume that these are simple sprites or
  other image files. Gender, Race and Class will determine the available portraits.
- Naming the character
- Saving the character

### Navigation

The player can use the arrow keys to navigate the options vertically. Certain menus will have hot keys:

- Gender: (M)ale, (F)emale, (O)ther
- Classes: (M)ele, (H)oly, (A)rcane, (S)tealth

Players can also use the back arrow to return to the previous menu. In addition, under the last option for each step should be a (P)revious to return to the previous menu (except for the first step)

### Character Sheet Display

As the player progresses through the character creation process, the character sheet will be updated. Make sure the values are properly capitalized. The skill section will require a separate interface divided by combat skills and non-combat skills.

- The Step section should display the step. It uses the CreationStep.NAME but the NAME portion needs to be properly cased and change the underscore to a space.
- Breadcrumb Navigation Bar
  - Ordering should show Gender, Race, Class
  - For Subrace and Subclass, use the format: Race / Subclass, Archtype / Class
  - Ensure that the values are properly capitalized

#### To Do

There will be additional steps for the character creation process such as multi-classing. Dual-classing will only be available after a character is created and reaches a certain level.

Once the player confirms saving a new character, the character will be saved to a JSON file in the saved_games directory as part of a characters.json file.

### Stats Rules for a Starting Character

- Attributes are based on a 1-20 point scale. Having less than 1 in an attribute will cause the character to instantly die (e.g. when a shadow hits a weak mage and causes the mage to have 0 or less strength). Attributes can exceed 20 through racial modifiers, equipment or other permanent means.
- When a character is being created, the race/subrace will determine the minimum base score. The class
  will further modify the minimum base score. An additional roll that adds 1-6 points to the base score will be given after a class is selected.
- In addition to the previous roll, a final bonus roll will be given to distribute the remaining points that can be used in any attribute for customization.
- There should be one additional roll for multiclassing. However, that system needs to be fleshed out further before figuring out what this number will be. The idea will be similar to the old Wizard's Crown
  game where one of the stats can determine the number of classes a character can multiclass into. But some
  subclasses will have higher number of points to prevent overly powerful single characters.
