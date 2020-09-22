# Koch Snowflake
The fractal 'Koch Snowflake' drawn with Python and Tkinter (pencil.py), and the coordinates generated using two approaches: my own flawed approach (customKochSnowflake.py), and a recursive complete approach stolen online (recursiveKochSnowflake.py).

The program is run by executing pencil.py, but by default nothing is drawn on the screen. One of the two out-commented lines in initUI() must be un-commented.. 

## My approach
I started out only looking at [this picture from Wikipedia](https://en.wikipedia.org/wiki/Koch_snowflake#/media/File:KochFlake.svg), and only being able to draw lines between coordinates in Tkinter. My approach then is to locate each edge and draw a triangle on it. We start with a triangle as seen on the picture from Wikipedia (albeit downward facing), and we then calculate the new vertices of the triangle on the horizontal edge; this is done using simple trigonometry as shown in [trimaths.jpg](https://github.com/ConanBacterium/Koch-Snowflake-/blob/master/documentation/trimaths.jpg?raw=true), and is implemented as the function genTriCoordsFromEdge(v1, v2, edgeLength, coeff). 

This however only works if the edge is in parallel with the x-axis. To get around this issue a change of basis is applied to v1 and v2, then the coordinates to the triangle on the edge between v1 and v2 are calculated, and then the basis of all the coordinates is changed back to the normal basis. Thus the first basisvector will be parallel with the edge and the second basisvector will be perpendicular to the edge - in effect the edge can be treated as if it was parallel with the x-axis, meaning that the function genTriCoordsFromEdge() will return the correct coordinates. 

The edges are recognized from a global list of vertices called vertices[]. It's important that the vertices are in sequence, as the program expects there to be an edge between each element of the list, including the first and last element. That is what sortVertices() is for. 

The next problem is the sequence in which the base must be rotated. To generate the second iteration the basis must be rotated 120 degrees clockwise (-2 pi / 3 radians) twice as shown on my notes [here](https://github.com/ConanBacterium/Koch-Snowflake-/blob/master/documentation/notes1.jpg?raw=true). (Remember that the change of basis is applied to make the edge of the previous iteration parallel with the x-axis, the rotations are NOT creating the vertices/angles of the new triangle).

To generate the third iteration the basis must alternate between 60 degrees CCW and 120 degrees CW as shown [here](https://raw.githubusercontent.com/ConanBacterium/Koch-Snowflake-/master/documentation/notes2.jpg).

At this point I realised that I would have to either hardcode the sequence of rotations for each iteration or I would have to find the pattern. The former seemed unfulfilling, and the second seemed too difficult - so I decided to cheat. 

## Stolen approach
So I googled something along the lines of "Python Koch Snowflake" and one of the first results was [this short youtube video](https://www.youtube.com/watch?v=RykDHleSTs0). I took a look at the code and converted it into [this pseudocode](https://github.com/ConanBacterium/Koch-Snowflake-/blob/master/documentation/pseudocode.png?raw=true). I then implemented the two functions also using my change-of-basis-approach. 
