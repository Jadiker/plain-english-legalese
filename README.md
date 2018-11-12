# plain-english-legalese
Purpose: Increase the accessibility and interpretability of law to the layperson

Usage and implementation summary: 
Our plain-english-legalese is designed as a tool to allow those with limited legal knowledge to better find resources to defend themselves against predatory hegemonic organizations and institutions. Our database provides a centrallized system for searching terms, both by scraping websites for relevant translations and by allowing registered users to edit terms themselves. Therefore, combining the resources of a credential system and the definitions of legal terms existing on the Internet, our project reduces the overhead required to understand complex legal documents and aims to help the most disadvantaged. 

We used the Python library, beautiful soup, to scrape existing websites for definitions. These definitions can be continually improved with registered users, who must login management system, which is managed by Python's pickleDB module (will move to SQL databse in future iterations). Users that just want to access definitions can search definitions with a search tool that pulls data/results/matches for the search. An edit-distance DP approach is used to give the closest relevant search results if the search yields no results in our database, allowing for a more robust and helpful search tool. 
