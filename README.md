This **map.py** module is made to generate an .html map about filmmaking using information about production places, years of filming,
names of films and some additional and folium for Python.

To use this module you need to have special file 'locations.list' with whole films database.
Processing this file can took a lot of time, so I made the demonstrating version of the same file **'demo.list'**
for 2007 and 2018 years.
****
As a result you will have a map in .html file with **two layers**:
1. Markers on filmmaking **locations with names** and additional inf.
2. **3 Circle Markers** for 3 countries of colors: 
* **red** - if this country have the biggest amount of films,
* **yellow** - if the number of films is average,
* **green** - if the number of films is the smallest.
 
****

**HTML tags:**
```html
<!DOCTYPE>  Defines the document type
<meta>      Defines metadata about an HTML document
<script>    Defines a client-side script
<link>      Defines the relationship between a document and an external resource (most used to link to style sheets)
<style>     Defines style information for a document
<div>       Defines a section in a document
<img>       Defines an image
<svg>	    Defines a container for SVG graphics
<i>	    Defines a part of text in an alternate voice or mood
<a>	    Defines a hyperlink
<path>      Defines a path.
```
****
**The conclusion:**
this module can help to analyze and compare film production of different years and countries showing whole information on **one picture**.