# project python files tree
> read the following files
> use the bellow project github source root link + file path listed bellow:

<https://github.com/Korck666/portal-chat-api/tree/production/>

```text
app/engine/ai_service.py
app/engine/database.py
app/engine/database_descriptor.py
app/engine/database_type.py
app/engine/document.py
app/engine/document_descriptor.py
app/engine/document_type.py
app/engine/game_system.py
app/engine/log_level.py
app/engine/retriever.py
app/engine/vector_database.py
app/engine/vector_database_retriever.py
app/engine/__init__.py
app/impl/databases/vector/descriptors/pinecone_descriptor.py
app/impl/databases/vector/pinecone_database.py
app/impl/dnd5_system.py
app/impl/Pathfinder_system.py
app/impl/__init__.py
app/main.py

Here is a brief summary of each file:

ai_service.py: This file defines the AIService class, which is an abstract base class for AI services. It has methods for connecting to the service, disconnecting, and performing operations like inserting, querying, and deleting documents.

database.py: This file defines the Database class, which is an abstract base class for databases. It has methods for connecting to the database, disconnecting, and performing operations like inserting, querying, and deleting documents.

database_descriptor.py: This file defines the DatabaseDescriptor class, which is a data class that holds information about a database, such as its name, host, and API key.

database_type.py: This file defines the DatabaseType enum, which lists the types of databases that the system can handle.

document.py: This file defines the Document class, which is a data class that represents a document in the system.

document_descriptor.py: This file defines the DocumentDescriptor class, which is a data class that holds information about a document, such as its ID and vector representation.

document_type.py: This file defines the DocumentType enum, which lists the types of documents that the system can handle.

game_system.py: This file defines the GameSystem class, which is an abstract base class for game systems. It has a method for applying the game system's rules to a game state.

log_level.py: This file defines the LogLevel enum, which lists the levels of logging that the system can handle.

retriever.py: This file defines the Retriever class, which is an abstract base class for retrievers. It has methods for connecting to the retriever, disconnecting, and performing operations like inserting, querying, and deleting documents.

vector_database.py: This file defines the VectorDatabase class, which is an abstract base class for vector databases. It extends the Database class and adds methods for creating and deleting indexes.

vector_database_retriever.py: This file defines the VectorDatabaseRetriever class, which is an abstract base class for vector database retrievers. It extends the Retriever class and adds a method for creating a retriever from a database descriptor.

pinecone_descriptor.py: This file defines the PineconeDescriptor class, which is a data class that holds information about a Pinecone database.

pinecone_database.py: This file defines the PineconeDatabase class, which is a class for interacting with a Pinecone database. It extends the VectorDatabase class.

dnd5_system.py: This file defines the DnD5GameSystem class, which is a class for applying the D&D 5 rules to a game state. It extends the GameSystem class.

Pathfinder_system.py: This file defines the PathfinderGameSystem class, which is a class for applying the Pathfinder rules to a game state. It extends the GameSystem class.

main.py: This file is the main entry point for the application. It sets up the FastAPI application, mounts the static files, and defines the routes for the application.
```
