import pathway as pw
from app.utils.config import NEWS_SOURCE_FILE, PATHWAY_HOST, PATHWAY_PORT
from app.rag.embeddings import embed_text

class StreamPipeline:
    def __init__(self):
        self.host = PATHWAY_HOST
        self.port = PATHWAY_PORT

    def run(self):
        # 1. Input Source: Watch a directory/file for changes
        # mode="streaming" ensures we process new lines as they appear
        documents = pw.io.fs.read(
            path=str(NEWS_SOURCE_FILE),
            format="json",
            mode="streaming",
            autocommit_duration_ms=500
        )

        # 2. Embedding: Apply the embedding UDF
        enricher = documents + list(embed_text(documents.text))
        
        # 3. Rename columns for clarity (optional but good for debugging)
        # This results in a table with columns: text, timestamp, source, vector
        # The result of the UDF is usually in a column named 'result' or simply appended if unwrapped.
        # Let's be explicit about the vector column.
        # embed_text returns a numpy array, we cast it to be sure.
        embedded_docs = documents.select(
            text=documents.text,
            timestamp=documents.timestamp,
            vector=embed_text(documents.text)
        )

        # 4. Create a KNN Index
        # This creates a searchable index on the 'vector' column
        index = pw.io.fs.write(
            embedded_docs,
            path="null", # We don't need to write the raw data to disk, we want to serve it
            format="null"
        ) 
        
        # Actually, for RAG, we want to run a server that exposes a KNN endpoint.
        # Pathway's latest RAG conventions use `pw.io.http.server` or similar, 
        # but for a custom KNN, we can use `pw.debug.compute_and_print` for local testing
        # or `pw.run` with a serving component.
        
        # A proper way in Pathway to expose a KNN lookup is often via `pw.io.http.add_endpoint`.
        # However, for simplicity in a hackathon, we can use the `KNNIndex` helper content 
        # or manually expose via a simple HTTP connector.
        
        # Let's use the standard `pw.io.http` to accept queries if we wanted to push queries in,
        # but here we want to answering queries. 
        
        # STRATEGY: We will spin up a Pathway server that serves the KNN index.
        # We'll use `pw.ml.index.KnnIndex` if available or simply serve the table
        # and do the join in the query step.
        
        # SIMPLIFIED APPROACH for Hackathon:
        # We will use `pw.io.http.rest_connector` to serve the table state? No.
        # We will use `pathway`'s ability to act as a server.
        
        # CORRECT APPROACH:
        # We will not confuse things. We will just run the pipeline and let it process.
        # BUT we need to QUERY it.
        # To query it from FastAPI, we need an Input Table for queries.
        
        pass 

def create_pipeline():
    """
    Constructs the pipeline and returns the queryable table or context.
    """
    # 1. Input: News Stream
    data = pw.io.fs.read(
        path=str(NEWS_SOURCE_FILE),
        format="json",
        mode="streaming",
        with_metadata=True
    )
    
    # 2. Embed content
    documents = data.select(
        text=pw.this.text,
        vector=embed_text(pw.this.text)
    )

    # 3. Input: Queries (Received via HTTP)
    # We create a table that listens on an HTTP endpoint for new queries
    query, response_writer = pw.io.http.rest_connector(
        host=PATHWAY_HOST,
        port=PATHWAY_PORT,
        schema=pw.schema_from_dict({"query": str, "k": int}),
        autocommit_duration_ms=50
    )

    # 4. Embed Queries
    query_vectors = query.select(
        query=query.query,
        k=query.k,
        vector=embed_text(query.query)
    )

    # 5. KNN Search (Dynamic RAG)
    # We join the queries with the documents based on vector similarity
    matches = query_vectors.join(
        documents,
        pw.left.vector.knn(pw.right.vector, k=pw.left.k),
        defaults={"text": "No data found"}
    ).select(
        query=pw.left.query,
        result=pw.right.text
    )

    # 6. Output: structured results back to the HTTP response
    # We group by query to formatting the list of results
    # For simplicity, we just return the matches directly. 
    # In a real app, we might JSON aggregate.
    response_writer(matches)
    
    return
    
if __name__ == "__main__":
    create_pipeline()
    print(f"Pipeline running on {PATHWAY_HOST}:{PATHWAY_PORT}")
    pw.run()
