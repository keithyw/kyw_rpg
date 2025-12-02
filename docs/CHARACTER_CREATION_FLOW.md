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
  will determine what available skills a character can choose from. We will need to determine a starting number of skill points that can be distributed. See Skill Section
  for details on how a character can choose skills or be
  automatically granted them on start.
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

### Skills Screen

After selecting the character class and assigning
attributes, the player will be taken to the skills screen.
There are two types of skills: combat and noncombat. The
list of available skills are derived from the combat_skills.json and noncombat_skills.json files.

At this time, the races.json file needs to be updated
to show which skills can be used. But for the classes.json
file, the way the combat and noncombat skills are made
available to a character is through an inheritance mechanism.

At the broadest level, the archetype contains the
base skills for subclasses. The "prohibited_combat_skills"
array will deduct the available combat skills. Classes
and specializations will inherit the skills and noncombat
skills from the archetype but can override those values.
For instance, the fighter archetype allows all combat
skills except wands. But a kensai specializtaion, lists
ranged, leather, chain, plate and shield as prohibited
which prevents the class from using most armor.

When a user enters the skills screen, they should see
the list of available skills as well as points assigned
to those skills. There might be default skills from the
class, race with a default amount of points assigned.
The base number of points that a player can spend
at this stage is 5 for combat and 5 for noncombat skills.
Default skills will not deduct from the starting point
value and be treated as a bonus.
