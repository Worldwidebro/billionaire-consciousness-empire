# RAG Indexer for IZA OS

Builds embeddings and vector indexes for the knowledge management system using ChromaDB and other vector databases.

## Features

- **Multi-source ingestion**: Support for various content types
- **Intelligent chunking**: Optimal text splitting with overlap
- **Vector embeddings**: High-quality embeddings generation
- **Database integration**: ChromaDB, Weaviate, Pinecone support
- **Metadata management**: Rich metadata and provenance tracking
- **Incremental updates**: Efficient index updates and maintenance

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG Indexer                             │
├─────────────────────────────────────────────────────────────┤
│  Content Ingestion                                          │
│  ├── File System Watcher                                   │
│  ├── API Endpoint Ingestion                                │
│  ├── Database Query Ingestion                              │
│  └── Real-time Stream Ingestion                            │
├─────────────────────────────────────────────────────────────┤
│  Content Processing                                         │
│  ├── Text Extraction & Cleaning                            │
│  ├── Intelligent Chunking                                  │
│  ├── Metadata Extraction                                    │
│  └── Content Validation                                     │
├─────────────────────────────────────────────────────────────┤
│  Embedding Generation                                       │
│  ├── Multi-provider Support (OpenAI, Local, HuggingFace)   │
│  ├── Batch Processing                                       │
│  ├── Embedding Caching                                     │
│  └── Quality Validation                                     │
├─────────────────────────────────────────────────────────────┤
│  Vector Database Integration                                │
│  ├── ChromaDB Integration                                   │
│  ├── Weaviate Integration                                   │
│  ├── Pinecone Integration                                   │
│  └── Custom Vector Store Support                            │
└─────────────────────────────────────────────────────────────┘
```

## Configuration

```python
RAG_CONFIG = {
    "chunking": {
        "chunk_size": 1000,
        "chunk_overlap": 200,
        "min_chunk_size": 100,
        "max_chunk_size": 2000
    },
    "embeddings": {
        "provider": "openai",  # openai, local, huggingface
        "model": "text-embedding-ada-002",
        "batch_size": 100,
        "cache_enabled": True
    },
    "vector_db": {
        "type": "chromadb",  # chromadb, weaviate, pinecone
        "host": "localhost",
        "port": 8000,
        "collection_name": "iza_os_knowledge"
    },
    "sources": {
        "obsidian": {
            "enabled": True,
            "path": "/Users/you/ObsidianVault",
            "sync_interval": 300  # 5 minutes
        },
        "apple_notes": {
            "enabled": True,
            "export_path": "./exports/apple_notes",
            "sync_interval": 600  # 10 minutes
        },
        "jupyter": {
            "enabled": True,
            "notebook_path": "./notebooks",
            "sync_interval": 1800  # 30 minutes
        }
    }
}
```

## Core Indexer Class

```python
class RAGIndexer:
    def __init__(self, config: dict = None):
        self.config = config or RAG_CONFIG
        self.chunker = IntelligentChunker(self.config["chunking"])
        self.embedder = EmbeddingGenerator(self.config["embeddings"])
        self.vector_db = VectorDatabase(self.config["vector_db"])
        self.metadata_extractor = MetadataExtractor()
        
        # Initialize file watchers
        self.file_watchers = {}
        self.setup_file_watchers()
    
    def setup_file_watchers(self):
        """Setup file system watchers for real-time ingestion"""
        for source_name, source_config in self.config["sources"].items():
            if source_config.get("enabled", False):
                watcher = FileWatcher(
                    path=source_config["path"],
                    interval=source_config.get("sync_interval", 300),
                    callback=self.process_source_files
                )
                self.file_watchers[source_name] = watcher
    
    async def build_index(self, source_path: str = None) -> dict:
        """Build complete RAG index from sources"""
        start_time = time.time()
        stats = {
            "total_files": 0,
            "total_chunks": 0,
            "total_embeddings": 0,
            "errors": 0,
            "processing_time": 0
        }
        
        try:
            # Get all source files
            if source_path:
                files = self.get_files_from_path(source_path)
            else:
                files = self.get_all_source_files()
            
            stats["total_files"] = len(files)
            
            # Process files in batches
            batch_size = self.config["embeddings"]["batch_size"]
            for i in range(0, len(files), batch_size):
                batch = files[i:i + batch_size]
                batch_stats = await self.process_file_batch(batch)
                
                # Update stats
                stats["total_chunks"] += batch_stats["chunks"]
                stats["total_embeddings"] += batch_stats["embeddings"]
                stats["errors"] += batch_stats["errors"]
            
            stats["processing_time"] = time.time() - start_time
            
            # Update index metadata
            await self.update_index_metadata(stats)
            
            logger.info(f"Index built successfully: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Index building failed: {e}")
            stats["errors"] += 1
            raise
    
    async def process_file_batch(self, files: list) -> dict:
        """Process a batch of files"""
        batch_stats = {"chunks": 0, "embeddings": 0, "errors": 0}
        
        for file_path in files:
            try:
                # Extract content and metadata
                content, metadata = await self.extract_file_content(file_path)
                
                if not content:
                    continue
                
                # Chunk content
                chunks = self.chunker.chunk_text(content, metadata)
                batch_stats["chunks"] += len(chunks)
                
                # Generate embeddings
                embeddings = await self.embedder.generate_embeddings(chunks)
                batch_stats["embeddings"] += len(embeddings)
                
                # Store in vector database
                await self.vector_db.store_chunks(chunks, embeddings, metadata)
                
            except Exception as e:
                logger.error(f"Failed to process file {file_path}: {e}")
                batch_stats["errors"] += 1
        
        return batch_stats
    
    async def extract_file_content(self, file_path: str) -> tuple:
        """Extract content and metadata from file"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.md':
            return await self.extract_markdown(file_path)
        elif file_ext == '.txt':
            return await self.extract_text(file_path)
        elif file_ext == '.json':
            return await self.extract_json(file_path)
        elif file_ext == '.ipynb':
            return await self.extract_jupyter(file_path)
        elif file_ext == '.html':
            return await self.extract_html(file_path)
        else:
            logger.warning(f"Unsupported file type: {file_ext}")
            return None, {}
    
    async def extract_markdown(self, file_path: str) -> tuple:
        """Extract content from Markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract frontmatter if present
            metadata = self.metadata_extractor.extract_frontmatter(content)
            
            # Clean content
            content = self.metadata_extractor.remove_frontmatter(content)
            
            # Add file metadata
            metadata.update({
                "source": file_path,
                "file_type": "markdown",
                "file_size": len(content),
                "last_modified": os.path.getmtime(file_path)
            })
            
            return content, metadata
            
        except Exception as e:
            logger.error(f"Failed to extract markdown from {file_path}: {e}")
            return None, {}
    
    async def extract_jupyter(self, file_path: str) -> tuple:
        """Extract content from Jupyter notebook"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            # Extract text from cells
            content_parts = []
            metadata = {
                "source": file_path,
                "file_type": "jupyter",
                "cell_count": len(notebook.get("cells", [])),
                "last_modified": os.path.getmtime(file_path)
            }
            
            for cell in notebook.get("cells", []):
                if cell.get("cell_type") == "markdown":
                    content_parts.append("".join(cell.get("source", [])))
                elif cell.get("cell_type") == "code":
                    # Include code with comments
                    code_content = "".join(cell.get("source", []))
                    content_parts.append(f"```python\n{code_content}\n```")
            
            content = "\n\n".join(content_parts)
            
            return content, metadata
            
        except Exception as e:
            logger.error(f"Failed to extract jupyter from {file_path}: {e}")
            return None, {}
```

## Intelligent Chunker

```python
class IntelligentChunker:
    def __init__(self, config: dict):
        self.chunk_size = config["chunk_size"]
        self.chunk_overlap = config["chunk_overlap"]
        self.min_chunk_size = config["min_chunk_size"]
        self.max_chunk_size = config["max_chunk_size"]
    
    def chunk_text(self, text: str, metadata: dict) -> list:
        """Intelligently chunk text with semantic awareness"""
        # Pre-process text
        text = self.preprocess_text(text)
        
        # Split by semantic boundaries
        semantic_chunks = self.split_by_semantic_boundaries(text)
        
        # Further split large chunks
        final_chunks = []
        for chunk in semantic_chunks:
            if len(chunk) <= self.chunk_size:
                final_chunks.append(chunk)
            else:
                sub_chunks = self.split_large_chunk(chunk)
                final_chunks.extend(sub_chunks)
        
        # Create chunk objects with metadata
        chunk_objects = []
        for i, chunk_text in enumerate(final_chunks):
            if len(chunk_text.strip()) >= self.min_chunk_size:
                chunk_obj = {
                    "id": f"{metadata.get('source', 'unknown')}_{i}_{hashlib.md5(chunk_text.encode()).hexdigest()[:8]}",
                    "text": chunk_text.strip(),
                    "metadata": {
                        **metadata,
                        "chunk_index": i,
                        "chunk_size": len(chunk_text),
                        "total_chunks": len(final_chunks)
                    }
                }
                chunk_objects.append(chunk_obj)
        
        return chunk_objects
    
    def split_by_semantic_boundaries(self, text: str) -> list:
        """Split text by semantic boundaries (paragraphs, sections, etc.)"""
        # Split by double newlines (paragraphs)
        paragraphs = text.split('\n\n')
        
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) <= self.chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def split_large_chunk(self, chunk: str) -> list:
        """Split large chunks with overlap"""
        if len(chunk) <= self.chunk_size:
            return [chunk]
        
        chunks = []
        start = 0
        
        while start < len(chunk):
            end = start + self.chunk_size
            
            # Try to break at sentence boundary
            if end < len(chunk):
                sentence_end = chunk.rfind('.', start, end)
                if sentence_end > start + self.min_chunk_size:
                    end = sentence_end + 1
            
            chunk_text = chunk[start:end].strip()
            if chunk_text:
                chunks.append(chunk_text)
            
            start = end - self.chunk_overlap
        
        return chunks
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for better chunking"""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
```

## Embedding Generator

```python
class EmbeddingGenerator:
    def __init__(self, config: dict):
        self.config = config
        self.provider = config["provider"]
        self.model = config["model"]
        self.batch_size = config["batch_size"]
        self.cache_enabled = config["cache_enabled"]
        
        # Initialize provider client
        self.client = self.initialize_client()
        
        # Initialize cache
        if self.cache_enabled:
            self.cache = EmbeddingCache()
    
    def initialize_client(self):
        """Initialize embedding client based on provider"""
        if self.provider == "openai":
            return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif self.provider == "local":
            return LocalEmbeddingClient()
        elif self.provider == "huggingface":
            return HuggingFaceEmbeddingClient(model=self.model)
        else:
            raise ValueError(f"Unsupported embedding provider: {self.provider}")
    
    async def generate_embeddings(self, chunks: list) -> list:
        """Generate embeddings for text chunks"""
        embeddings = []
        
        # Process in batches
        for i in range(0, len(chunks), self.batch_size):
            batch = chunks[i:i + self.batch_size]
            batch_embeddings = await self.generate_batch_embeddings(batch)
            embeddings.extend(batch_embeddings)
        
        return embeddings
    
    async def generate_batch_embeddings(self, chunks: list) -> list:
        """Generate embeddings for a batch of chunks"""
        batch_embeddings = []
        
        for chunk in chunks:
            # Check cache first
            if self.cache_enabled:
                cached_embedding = self.cache.get(chunk["text"])
                if cached_embedding:
                    batch_embeddings.append(cached_embedding)
                    continue
            
            # Generate new embedding
            try:
                embedding = await self.generate_single_embedding(chunk["text"])
                
                # Cache embedding
                if self.cache_enabled:
                    self.cache.set(chunk["text"], embedding)
                
                batch_embeddings.append(embedding)
                
            except Exception as e:
                logger.error(f"Failed to generate embedding for chunk {chunk['id']}: {e}")
                # Use zero embedding as fallback
                batch_embeddings.append([0.0] * 1536)  # OpenAI embedding dimension
        
        return batch_embeddings
    
    async def generate_single_embedding(self, text: str) -> list:
        """Generate embedding for single text"""
        if self.provider == "openai":
            response = await self.client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding
        
        elif self.provider == "local":
            return await self.client.generate_embedding(text)
        
        elif self.provider == "huggingface":
            return await self.client.generate_embedding(text)
        
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
```

## Vector Database Integration

```python
class VectorDatabase:
    def __init__(self, config: dict):
        self.config = config
        self.db_type = config["type"]
        self.collection_name = config["collection_name"]
        
        # Initialize database client
        self.client = self.initialize_client()
    
    def initialize_client(self):
        """Initialize vector database client"""
        if self.db_type == "chromadb":
            return ChromaClient(
                host=self.config.get("host", "localhost"),
                port=self.config.get("port", 8000)
            )
        elif self.db_type == "weaviate":
            return WeaviateClient(
                url=self.config.get("url", "http://localhost:8080")
            )
        elif self.db_type == "pinecone":
            return PineconeClient(
                api_key=self.config.get("api_key"),
                environment=self.config.get("environment")
            )
        else:
            raise ValueError(f"Unsupported vector database: {self.db_type}")
    
    async def store_chunks(self, chunks: list, embeddings: list, metadata: dict):
        """Store chunks with embeddings in vector database"""
        if self.db_type == "chromadb":
            await self.store_chromadb(chunks, embeddings, metadata)
        elif self.db_type == "weaviate":
            await self.store_weaviate(chunks, embeddings, metadata)
        elif self.db_type == "pinecone":
            await self.store_pinecone(chunks, embeddings, metadata)
    
    async def store_chromadb(self, chunks: list, embeddings: list, metadata: dict):
        """Store in ChromaDB"""
        collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "IZA OS Knowledge Base"}
        )
        
        # Prepare data for ChromaDB
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        ids = [chunk["id"] for chunk in chunks]
        
        # Add to collection
        collection.add(
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
            ids=ids
        )
    
    async def query(self, query_text: str, n_results: int = 5, filter_metadata: dict = None) -> list:
        """Query vector database for similar content"""
        if self.db_type == "chromadb":
            return await self.query_chromadb(query_text, n_results, filter_metadata)
        elif self.db_type == "weaviate":
            return await self.query_weaviate(query_text, n_results, filter_metadata)
        elif self.db_type == "pinecone":
            return await self.query_pinecone(query_text, n_results, filter_metadata)
    
    async def query_chromadb(self, query_text: str, n_results: int, filter_metadata: dict) -> list:
        """Query ChromaDB"""
        collection = self.client.get_collection(self.collection_name)
        
        # Generate query embedding
        query_embedding = await self.generate_query_embedding(query_text)
        
        # Query collection
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_metadata
        )
        
        # Format results
        formatted_results = []
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            formatted_results.append({
                "rank": i + 1,
                "text": doc,
                "metadata": metadata,
                "similarity_score": 1 - distance
            })
        
        return formatted_results
```

## Usage Examples

### Build Complete Index
```python
# Initialize indexer
indexer = RAGIndexer()

# Build index from all sources
stats = await indexer.build_index()
print(f"Index built: {stats['total_chunks']} chunks from {stats['total_files']} files")
```

### Build Index from Specific Path
```python
# Build index from specific directory
stats = await indexer.build_index("/path/to/specific/source")
```

### Query Index
```python
# Query the index
results = await indexer.vector_db.query(
    query_text="What is IZA OS architecture?",
    n_results=5,
    filter_metadata={"file_type": "markdown"}
)

for result in results:
    print(f"Rank {result['rank']}: {result['similarity_score']:.3f}")
    print(f"Text: {result['text'][:200]}...")
    print(f"Source: {result['metadata']['source']}")
    print("-" * 50)
```

### Real-time Indexing
```python
# Start file watchers for real-time indexing
for watcher in indexer.file_watchers.values():
    watcher.start()

# The indexer will automatically process new files as they're added
```
