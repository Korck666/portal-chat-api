# portal-chat-api

<!-- ![PORTAL CHAT API](./static/logo_rpg_portal.png "PORTAL CHAT API") -->
<img src="./app/static/logo_rpg_portal.png" alt="MarineGEO circle logo" style="height: 100px; width:100px;"/>

## READ AND USE IT TO GET HELP FROM CHATGPT AND GITHUB COPILOT

This is the REST API service that encapsulates multiple AI services, including ChatGPT and potentially Dall-E, and also manages game rules and database connections. 
This is a complex task that involves several components, and it would be best to approach it using a combination of design patterns. 
Here are some design patterns that we will use to build this service:

1. **Facade Pattern**: This pattern provides a unified interface to a set of interfaces in a subsystem. We can use this pattern to create a simplified API for the various AI services we're using. This way, the rest of our application doesn't need to know about the specifics of interacting with these services.

2. **Factory Pattern**: This pattern provides an interface for creating objects in a superclass but allows subclasses to alter the type of objects that will be created. We can use this pattern to create instances of different AI services based on the game's needs, for instance.

3. **Singleton Pattern**: This pattern ensures that a class has only one instance and provides a global point of access to it. However, there are few points I consider using this pattern, such as for the service that manages the database connections, ensuring that only one connection is active at any given time to a specific service (URL: port) and managing connection pools.

4. **Strategy Pattern**: This pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. We can use this pattern to manage different game rules, for instance, allowing the game to have different pre-made game-systems (D&D5, D&D4, PathFinder, Cyberpunk, etc.), also we want to allow players to homebrew their own systems.

As for writing clean and efficient code in Python, we are going to use LangChain for core orchestration of models, memory, prompt templates, tools, flows etc.
We are using FastAPI to provide the REST API interface along with auto-documentation and an easy integrated web testing package.

Following, please find some more guidelines that we need to implement into automation checks (github actions):

1. **Follow the DRY Principle**: Don't Repeat Yourself. If you find yourself writing the same code more than once, consider turning it into a function or method.

2. **Use Pythonic Conventions**: Python has a set of conventions and idioms that make code more readable and efficient, such as list comprehensions and the use of `is` for identity comparison.

3. **Use LangChain's Modules**: LangChain provides several modules like Models, Prompts, Memory, Indexes, Chains, Agents, and Callbacks. Use these modules effectively to build your application.

4. **Leverage FastAPI's Features**: FastAPI provides several features like API VERSIONING and compatibility handling, dependency injection, automatic request validation, and asynchronous request handling. Make sure to use these features to write efficient and clean code.

5. **Test Your Code**: Write tests for your code to ensure it behaves as expected. This is especially important when working with complex systems like AI and databases. (*We need to decide for a good Python framework here ASAP)

6. **Document Your Code**: Make sure to write clear CODE which makes comments and documentation for your code meaningless, but even that do comment whenever you feel it makes sense! This will make it easier for others (and the future you) to understand what your code is doing and certainly will mean a much better code. Remember, we read code in a proportion around a 10:1 in relation to writing, so make it readable.
