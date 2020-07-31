# Cakebored

## Objective

Build a cool, ergo, split keyboard.

Try not to spend too much.

## Features

These are my personal requirements for this keyboard. P number is Priority of the feature, lower is higher priority.

* P0: Custom ergonomic design - parameterized forward kinematic key positioning.
* P0: Split keyboard with thumb clusters.
* P0: Left half can operate as an independent keyboard.
* P0: Programable (i.e. QMK firmware)
* P0: Hot swap key switches
* P0: RGB per key and under lighting.
* P1: USB A hub in keyboard
* P1: Modular 3d print design that allows for some adjustment of parts
* P1: Customizable tilting of halves
* P1: Customizable positioning of thumb clusters
* P1: Socketed micro controller - easily changeable
* P1: Ability to switch to a different microcontroller
* P2: Customizable tilting for individual finger key columns
* P2: Wireless
* P2: Rotary encoder input
* P2: OLED displays
* P2: support non-1u sized keycaps

## Background

It’s COVID-19 quarantine work from home time! I was somehow convinced to get an Ergonox Ez keyboard. 
This led me down a rabbit hole of programmable, ergonomic keyboards. I was not super happy about the 
size and the thumb cluster layout. The [Dactyl Manuform](https://github.com/abstracthat/dactyl-manuform)
layout looks similar but not entirely like something I would like to try out.

### My skills assessment
Here’s my set of skills that led me to believe I can take on this project:

* Programming: advanced
* Embedded programming: intermediate
* 3d design and printing: intermediate to advanced
* Soldering: intermediate
* Electronics design: no experience
* Ordering parts off the internet: intermediate

## Research

This section keeps track of open questions and answered questions while doing research
into parts, libraries and techniques to use.

### Open Questions

#### How does an IO expander work? Dactyl / ergodox uses a teensy 2.0 on the primary side and an MCP23018 16 bit IO Expander on the secondary side.

#### What is I2C? SPI protocols?

#### [Learning how to use KiCAD](https://www.youtube.com/watch?v=c2niS9ZRBHo&list=PL3bNyZYHcRSUhUXUt51W6nKvxx2ORvUQB&index=2)

#### [Learning how to use FreeCAD](https://wiki.freecadweb.org/Getting_started) [programming](https://wiki.freecadweb.org/Macros)

### Answered Questions

#### Should I use some ESP32 controllers I happen to have on hand?

For this first build, keep it simple and use a microcontroller a lot of other people have used, namely, the Arduino pro micro.

#### What are the differences between various 1N4007, 1N4148, etc diodes and which one to use? 

These two have different breakdown characteristics. General consensus on keyboard usage is the 1N4148. There are also other 
[types of diodes](https://www.youtube.com/watch?v=kLX4ZFzzFDg) that should be avoided.

#### Use other fancy inputs or outputs?

Can use encoders (knobs), oled displays.

Stick to basics for this first build.

#### Can I actually solder small SMD components?

Tested this out on an old board I had laying around. Yes, seems doable.

#### Should I harvest old but fully functional mechanical keyboards for parts? (switches, caps)

Lets not do that and just buy new parts.

#### Do I need to panelize the key switch PCB? How do I do this?

No. Turns out that this doesn’t save any money. Also, manufacturers offer panelization options. 
There are also scripts to panelize the design in KiCAD.

#### Do I need to flash both sides of the keyboard if I have a microcontroller on each side?

[Yes, sometimes.](https://docs.splitkb.com/hc/en-us/articles/360011949679-When-do-I-need-to-flash-my-microcontroller-#:~:text=Split%20keyboards%20with%20two%20controllers,already%20when%20you%20get%20it.)

#### Can I make automatic interchangeable primary / secondary and  also independent halves?

Yes, there is [precedence](https://www.reddit.com/r/MechanicalKeyboards/comments/bh1q5y/split_keyboard_underglow_with_interchangable/).

### Microcontrollers

TODO: copy over research from doc.

### Case

#### Key Layout

While the Dactyl and various derivatives (e.g. maniform) seem to be pretty interesting, I want to try a
different, more personalized approach. I also was not interested in learning clojure/openSCAD. Going 
through the FreeCAD Python scripting system, it seems like something that would be easier to pick up and
work with. I also wanted to be able to customize the look of the case, the shape of the various Dactyls
I had seem were not great.

<b>Bonus ideas:</b> use actual keys along the top edge of the keyboard and double as status indicator LED / under 
keyboard glow.

#### Case Features

Want to build a case with modularized components rather than a monolithic single print.

* Possibly make minor repositions the finger key columns and thumb cluster.
* Legs to adjust tenting and angling e.g. Ergdox Ez
* Tray for microcontroller so that it can be replaced or upgraded
* Being able to easily customize where the various TRRS and USB port locations are.

## Build

This section details the ordering of parts and actual build process.

### Electronics

### Case

I have 3d printer, like using PETG, so will use that.

Want to try finishing using an epoxy coat. Purchased some tabletop epoxy.

### Parts List

Per key costs:

| part | vendor | quantity | price | shipping | Per Quant |
|------|--------|----------|-------|----------|-----------|
| switch pcb      | jlcpcb     | 200 | $15.70 | $9.36  | $0.13 |
| keycaps         | aliexpress | 200 | $50.21 | $0.00  | $0.25 |
| switches        | kbdfans    | 80  | $80.00 | $24.00 | $1.30 |
| hotswap sockets | kbdfans    | 200 | $20.00 |        | $0.10 |
| 1N4148 diodes   | aliexpress | 600 | $5.38  |        | $0.01 |
| leds SK6812mini | aliexpress | 300 | $23.92 |        | $0.08 |


Per split half keyboard costs:

| part | vendor | quantity | price | shipping | Per Quant |
|------|--------|----------|-------|----------|-----------|
| nuts, bolts, etc | various    | 10  | $50.00 |       | $5.00  |
| trrs socket      | aliexpress | 10  | $10.19 |       | $1.02  |
| filament         | amazon     | 1   | $20.00 |       | $20.00 |
| epoxy            | amazon     | 10  | $40.00 |       | $4.00  |
| epoxy color      | amazon     | 100 | $17.00 |       | $0.17  |
| electricity      | pg&e       | 1   | $10.00 |       | $10.00 |
| ic socket        | aliexpress | 10  | $1.83  | $2.32 | $0.42  |
| usb cable        | aliexpress | 4   | $5.14  |       | $1.29  |
| micro controller | aliexpress | 6   | $25.39 |       | $4.23  |

Infrastructure costs:

| part | vendor | quantity | price | shipping | Per Quant |
|------|--------|----------|-------|----------|-----------|
| 3d printer        |  | 100  | $800.00 |  | $8.00 |
| Soldering Station |  | 1000 | $400.00 |  | $0.40 |
