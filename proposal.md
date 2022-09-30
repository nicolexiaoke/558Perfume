# domain
We plan to build a knowledge graph about perfumes. The knowledge graph will include information about perfume's brand, name, smell, selling platform, volume, price, user feedbacks, ratings, deliverty, photos, etc. This knowledge graph will be useful because it is always tiring for people to compare different perfumes over different platforms with all of their different features. Thus, our KG can save people a lot of energy when they are strugling to decide which perfume to buy. 
We plan to use this knowledge graph to figure out what the most popular perfumes are, link identical perfume items between different selling platforms, as well as compare features like price, ratings, delivery and some other features to give users recommendations based on users preference.  


# dataset
Datasets: The knowledge graph will contain data mined from general online shopping sources like Amazon, Ebay, Sephora, FragranceNet, and some brands' official websites. 

# technical challenge

We might meet following techical challenges:

- Issues with crawlers on the website.
- Issues with entity linking problems.
- Deduplicate and data lacking.

Here's the detailed explannation:

The first possible technical challenge we will meet is the powerful anti-crawler when crawling the data from sells website. Some Website may have login requirement, we have to save cookies or use some tricks to get the comments, rating, and some other detailed info.

Then the entity linking challenge. Some products may have very different titles and they are not likely to linked with each other through title although they are the same entities, while others may have similiar titles but not likely to be same entities.

Deduplicate and data lacking. Some entities may lack of data while others may appear duplicate on several platforms.


