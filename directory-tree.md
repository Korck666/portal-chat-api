# tree -I "$(grep -v '^#' .gitignore | tr '\n' '|')" -I "__pycache__" > directory-tree.md

```text
.
├── Dockerfile
├── LICENSE
├── README.md
├── READMEFASTAPI.md
├── app
│   ├── engine
│   │   ├── __init__.py
│   │   ├── ai_service.py
│   │   ├── database.py
│   │   ├── database_descriptor.py
│   │   ├── database_type.py
│   │   ├── document.py
│   │   ├── document_descriptor.py
│   │   ├── document_type.py
│   │   ├── game_system.py
│   │   ├── log_level.py
│   │   ├── retriever.py
│   │   ├── vector_database.py
│   │   └── vector_database_retriever.py
│   ├── impl
│   │   ├── Pathfinder_system.py
│   │   ├── __init__.py
│   │   ├── databases
│   │   │   └── vector
│   │   │       ├── descriptors
│   │   │       │   └── pinecone_descriptor.py
│   │   │       └── pinecone_database.py
│   │   └── dnd5_system.py
│   ├── main.py
│   ├── scripts
│   │   └── postcommand.sh
│   └── static
│       ├── favincon16.png.png
│       ├── favincon32.png.png
│       └── logo_rpg_portal.png
├── compose-dev.yaml
├── directory-tree.md
├── openapi.json
├── requirements.txt
└── templates
    ├── worldCreation.json
    └── worldCreationExample.json

9 directories, 33 files

