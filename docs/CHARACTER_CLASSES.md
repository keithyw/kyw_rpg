# Character Classes

In this game, character classes operate on a system of archetypes, classes, and specializations that is heirarchical and inheritable. Each level below overrides
certain properties from the one above. For instance,
a fighter has a set of minimum attributes inside of the
required_attributes object such as STR: 9 and VIT: 9. A
mercenary has a STR: 10, which has the character have
at least 1o in STR. Likewise, a kensai character cannot
use most armor except cloth as enumerated in the prohibited_combat_skills array.

## Archetype

The archetype consists of one of four classes:

- Fighter
- Believers
- Spell Casters
- Underground

There are two properties under the archetype:

- core
- classes

### Core

Core are the baseline properties of all classes within
the archetype. These may be overridden by classes and
specializations. Under core are the following properties
that are common to all classes within the archetype:

- hp: a random amount specified by a die roll
- combat_skills: an object containing combat skills from the combat_skills.json file
- noncombat_skills: an object containing noncombat skills from the noncombat_skills.json file
- prohibited_combat_skills: an array containing combat skills that are prohibited for this class. The skills are
  referenced by the combat_skills.json file.
- required_attributes: an object containing the minimum attribute scores required for this class

### Classes

Classes are an object containing as the keys/properties
the names of the classes for an archetype. Each class
contains an object with the following properties:

- name: the display name of class
- description: a description of the class
- required_attributes: an object containing the minimum attribute scores required for this class. This can be
  empty if no additional attributes are required.
- prohibited_combat_skills: an array containing combat skills that are prohibited for this class.
- specializations: an object containing subclasses.

#### Specializations

Specialization contain additional overrides for a subclass.
Specializations provide a flavor for a class.

The following properties are available for specializations:

- name: the display name of specialization
- description: a description of the specialization
- required_attributes: an object containing the minimum attribute scores required for this specialization. This can be empty if no additional attributes are required.
- combat_skills: an object that has provides a list of skills that will be added to a character upon creation along with the starting value.
- noncombat_skills: an object that has provides a list of skills that will be added to a character upon creation along with the starting value.
- prohibited_combat_skills: an array containing combat skills that are prohibited for this specialization.

## Notes

- values specified by the "\*" imply "all" such as all combat skills.
- required_attributes keys refer to the attribute.json file
- not all values have been filled out.
