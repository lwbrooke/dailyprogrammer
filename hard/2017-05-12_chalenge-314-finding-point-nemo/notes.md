# brute force

calculate min distance from every ocean to every land, output point with largest distance

## optimization

figure out coastal land tiles, and only compare against those, rather than every land tile

# greedy approach (?)

we know that any water tile touching land while there are still tiles that aren't touching
land are not the furthest away from land, so they can be eliminated. Repeat this process
unitl there is only one point remaining. tally each "ring" to find the approximate distance
to land from the remaining point.
