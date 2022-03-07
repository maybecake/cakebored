# Eng design

## Keyboard Structure

There are several aspects of the keyboard structure:
1. General shape of the keyboard
1. Key positioning
1. Webbing between each key base


### Coordinate system

Put your left hand flat on the table, the coordinate system looks like this:

```
     | | | |          ^
     | | | |  /       |
     | | | | /        Y
     O O O O        <Z|-X->  (Z is going AWAY from you!)

```

For those, like me, who have trouble mapping coordinates to space, this means:

* Positive X = towards the thumb.
* Positive Y = further away from the user, towards top row of keys.
* Negative Z = higher off the table.
* Using X_AXIS as a rotation vector, negative angles tilt the keys
towards the user.

Since the two half of the keyboard are likely to be symmetrical, only the left
hand needs to be considered. If the two sides are NOT symmetrical, it should be
easy to generate a new layout based on the right hand measurements and just
mirror the final output model.

### Key positioning

There are three types of key positions:
1. Standard below regular finger key columns.
1. Extended key columns for index and pinky fingers.
1. Thumb keys / cluster

General principle is to generate the positioning of all keys based on forward
kinematics.

The finger.py module contains classes that calculate and store the positions for
the keys. Finger measurements are fed into the Finger classes to generate the
positions.

An initial idea was to use differences in finger position and angle to calculate
the angle used to depress a key. However, in practice, this doesn't seem to be
very ~useful~ correct and is overly complicated. A simplified manually entered
angle is used instead.

### Webbing

The individual key structure for retaining the key PCB, switch and key caps were
modeled by hand. (Maybe we should switch to doing this programmatically?). These
key bases all need to joined together to form the 3d shell of the keyboard.

The key_base.py module contains classes that generates this shell based on the
key positions generated from finger.py.