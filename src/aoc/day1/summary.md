This coding exercise primarily focuses on text processing and is therefore a great chance to use regular expressions (regex).

The task involves parsing a calibration document containing a mix of numeric digits and spelled-out digit names. Regex can efficiently identify both types of elements. A key challenge arises from the overlapping of spelled-out digits (like "oneight" for "1" and "8"). Python regex will not easily find overlapping matches.

To address this, I construct a dictionary that maps these overlapping cases to different numeric values depending on if the match is "first" or "last". I feel like this is an acceptable approach for a frist pass but after researching I discoverd that a lookahead with a capture group might have been more straightforward (though probably not more efficient.) See [this stack overflow](https://stackoverflow.com/a/5616910).

In general I think this is a fun exercise to showcases proficiency in regex, dictionary manipulation, and developing creative solutions to text processing problems.