import asyncio
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sherry_agent.memory.long_term import LongTermMemory

async def test_db_init():
    print("Testing database initialization...")
    # Use file-based database instead of in-memory
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        long_term_memory = LongTermMemory(db_path=db_path)
        await long_term_memory.initialize()
        print("Database initialized successfully")
        
        # Test adding a memory
        memory_id = await long_term_memory.add_memory("Test memory", {"type": "test"})
        print(f"Added memory with ID: {memory_id}")
        
        # Test getting memory count
        count = await long_term_memory.get_memory_count()
        print(f"Memory count: {count}")
        
        # Test searching memory
        results = await long_term_memory.search_memory("Test")
        print(f"Search results: {len(results)}")
        for result in results:
            print(f"  - {result['content']}")
    finally:
        # Clean up temporary file
        import os
        if os.path.exists(db_path):
            os.unlink(db_path)

if __name__ == "__main__":
    asyncio.run(test_db_init())
