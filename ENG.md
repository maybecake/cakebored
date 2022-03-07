# Eng design

## Keyboard Structure

There are several aspects of the keyboard structure:
1. General shape of the keyboard
1. Key positioning
1. Webbing between each key base


### Coordinate system

 Coordinate system assumes hand looks like this:

```
     | | | |          ^
     | | | |  /       |
     | | | | /        Y
     O O O O        <Z|-X->  (Z is going away from you!)

```

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

An initial idea was to use differences in angle to calculate the angle used to
depress a key. However, in practice, this doesn't seem to be very ~useful~
correct and is overly complicated. A simplified manually entered angle is used
instead.

### Webbing

The individual key structure for retaining the key PCB, switch and key caps were
modeled by hand. (Maybe we should switch to doing this programmatically?). These
key bases all need to joined together to form the 3d shell of the keyboard.

The key_base.py module contains classes that generates this shell based on the
key positions generated from finger.py.