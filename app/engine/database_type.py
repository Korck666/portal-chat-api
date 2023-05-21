# database_type.py
from enum import Enum

# Our core orchestrator will need to know what type of database it is working with
#   in order to properly interact with it. This enum will be used to represent the
#   different types of databases that our orchestrator will be able to interact with.
# We are using LangChain as this core orchestrator's andbased on the current versions,
#   it seems that LangChain does not explicitly list the types of memory or databases
#   it uses. However, common types of databases used in similar contexts include:


class DatabaseType(Enum):
    # Relational Databases: These databases store data in tables with rows and columns.
    #   They are highly structured and are often used for transactional purposes. Examples
    #   include MySQL and PostgreSQL.
    RELATIONAL = "relational"

    # Document Databases: These databases store data in documents, which are similar to
    #   JSON objects. They are highly flexible and are often used for content management
    #   and real-time analytics. Examples include MongoDB and CouchDB.
    DOCUMENT = "document"

    # Graph Databases: These databases store data in nodes and edges, which are used to
    #   represent relationships between data. They are highly scalable and are often used
    #   for social networking and recommendation engines. Examples include Neo4j and OrientDB.
    GRAPH = "graph"

    # Key-Value Databases: These databases store data as a collection of key-value
    #   pairs, where each key is unique. They are highly scalable and are often used
    #   for caching and storing large amounts of data. Examples include Redis and DynamoDB.
    KEY_VALUE = "key_value"

    # In-Memory Databases: These databases store data in the main memory (RAM) of the
    #   computing environment to provide faster response times. They are often used for
    #   real-time applications that require high-speed data access. Examples include Memcached
    #   and Hazelcast.
    IN_MEMORY = "in_memory"

    # Vector Databases: These databases are designed to handle vector data, which is essential
    #   for handling AI and machine learning workloads. Examples include Pinecone and Faiss.
    VECTOR = "vector"
