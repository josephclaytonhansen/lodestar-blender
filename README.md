## Lodestar for Blender 2.8

### What is this? 
Lodestar is a plugin to streamline sharing, copying, and re-using complex node trees. Lodestar is essentially a translator- the Lodestar language turns node trees into plain, linear, text. The Lodestar plugin takes that plain text and converts it into nodes.

### Why?
The advantage here is mainly ease and quality of life. Taking screenshots and sharing .blend files as a way to share nodes is just... the worst. It's time-consuming, memory consuming, and deeply inefficient. Thus, the Lodestar language is designed to be easy and quick to write; a shorthand, if you will. 

In future, this plugin will allow you to select a node tree and automatically convert it into plain text (and then back again!!) but right now, it's still very much under construction. In other words, **if you load this into Blender right now, it's not going to do much!**  

### Features
Features for stable launch: 
* Two-way conversion
* Automatic connection
* Automatic re-arranging/offset
* User interface

Planned features for upcoming updates:
* Access the references from a server- no memory lost, and always 100$ up to date
* Comp nodes
* "Favorites"

### Notation Rules (in plain easy English) 
* Period to the left: an input
* Period to the right: an output 
* Forks are marked by pn(n = 0,1,2...)
* If not forked, an input will always go to the first listed attribute (if there are attributes)
* Two slashes separates nodes 
* One slash separates attributes 
* One dash defines attributes per node
* Two periods makes a straight path 
* Nodes and attributes are shortened to four letters plus designation  
* Nodes are designated noden (n = 0,1,2...)
* Attributes are designated attrn (n = 0,1,2...)
* Numerical input is designated with dashes on either side plus applicable periods
* Paths end with =

For example, 
> rgba0..diff0-color/p1.rough//..glos0-color/p1.rough//=itex.p1=diff0.mixs0-slot1=glos0.mixs0-slot2=p1.mixs0-fac=mixs0.mato-surface=

combines diffuse and glossy, sharing an RGB color, with an image texture as roughness and mix factor. It may look complicated, but it's honestly fairly intuitive to write with a little practice. All special characters have been chosen to avoid usage of the shift key, as well, making it even faster. (That assumes you have a numberpad for symbols such as +.) 
