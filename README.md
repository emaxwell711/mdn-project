p1 represents a "player" and p2 represents the "conductor" in our DSCP (Dynamic Signal Configuration Protocol)
DSCP_Classes contains the Classes for various packet configurations, such as the DSCP Offer or DSCP ACK packets 
Utilities contains the various functions intended for implementation in the protocol, such as:

chooseBits - A function that takes as input a sequence of bits (a string of 0 
and 1) and "chooses" randomly only one bit among those set to 1, and 
returns another sequence of bits (another string) having the same length 
as the input, but with only one bit set to 1 and the others set to 0. 
Example: input "0101" possible output "0100" or "0001"; input 
"1011101001" possible output "1000000000" or "0010000000" or 
"0001000000" etc

SplitBits - A function that takes as input a sequence of 32 bits and returns 
3 separate strings, the first one with the first 5 bits, the second one 
with the next 4 bits, the third one with the remaining 23 bits

alphaBits - A function that takes as input a sequence of 16 bits and returns 
a lowercase letter for every bit set to 1 in the bit sequence. The 
letter must be the one having the same position in the alphabet as the 
'1' in the bit sequence. Example: input "1000000000000000" output "a"; 
input "0100000000000000" output "b"; input "0010000000000000" output 
"c"; [...] ; input "0000000000000001" output "p"
Extension: handle multiple 1's. Example: input "1100000000000000" output 
"ab"; input "0010000000000001" output "cp"

ConCatStrings - A function that, given 3 separate strings, checks that they are 
respectively 5, 4 and 23 characters long (otherwise raise an error), and 
concatenates the strings in a single one, and returns it.

CheckSeq - A function that, given 2 sequences of bits having the same 
length, checks if the two sequences have a '1' in common (a bit set to 
one in the same position), and return the position of that '1'. Raise an 
error if they don't have any '1' in the same position. Example: input 
"0011" and "0010", output 2 (the '1' in common is at position 2 in both 
strings); input "0011" and "0001" output 3 (the '1' in common is at 
position 3 in both strings); input "0100" and "0001" output Error (the 
two strings do not have a '1' in the same position)
