# factorioCalc
class based recurrent calculator for crafting efficency for Factorio that lets you calculate how many of a resource you need to craft with specific efficency

# usage
### initialisation
select resources on your main bus that you want to count, select types of furnaces you're using, select level of assembling machines and then for use simply create object of a class of item you're interested in, as an argument for initialisation change initCraftedPerSecond to destined amount per second
### crafting tree
i overloaded string form of class so all you need to do is print it to get full crafting tree
### combined resources
to get all resources combined for destined efficency declare object and call its getIngredients() function

# requirements
python - obviously
colorama - library im using for coloring certain resources
