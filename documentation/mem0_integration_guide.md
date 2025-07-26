# MEM0 Integration Guide for OBJX Platform

## Overview

This guide explains how to properly integrate MEM0 with the OBJX Platform to leverage its advanced AI memory capabilities. MEM0 provides sophisticated memory organization and retrieval systems specifically designed for AI engines, which are essential for the OBJX Platform's tier-based memory functionality.

## Prerequisites

1. Active MEM0 subscription
2. Valid MEM0 API key
3. Python 3.6+ environment

## Installation

Install the MEM0 Python SDK:

```bash
pip install mem0ai
```

## Configuration

1. Set your MEM0 API key in the `.env` file:

```
MEM0_API_KEY=your_mem0_api_key_here
```

2. Ensure the `mem0_client.py` file is in your backend directory.

## Tier-Based Memory Structure

The OBJX Platform uses a tier-based memory system:

- **Tier 1**: No memory capabilities
- **Tier 2**: Basic memory capabilities (conversation history, simple retrieval)
- **Tier 3**: Advanced memory capabilities (semantic search, context-aware retrieval)

## Usage

### Initializing the Memory Client

```python
from mem0_client import get_memory_client

# For Tier 1 user (no memory)
tier1_client = get_memory_client(user_tier=1, user_id="user123")

# For Tier 2 user (basic memory)
tier2_client = get_memory_client(user_tier=2, user_id="user456")

# For Tier 3 user (advanced memory)
tier3_client = get_memory_client(user_tier=3, user_id="user789")
```

### Adding Memories

```python
# Example conversation
messages = [
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."}
]

# Add to memory with metadata
memory_id = memory_client.add_memory(messages, {"topic": "geography"})
```

### Searching Memories

```python
# Search for relevant memories
results = memory_client.search_memory("France")

# Process results
for result in results:
    print(f"Memory: {result.get('content')}")
    print(f"Metadata: {result.get('metadata')}")
```

### Retrieving Recent Memories

```python
# Get recent memories
recent_memories = memory_client.get_recent_memories(limit=5)
```

## Advanced MEM0 Features

MEM0 provides several advanced features that enhance the OBJX Platform:

### Semantic Search

MEM0's semantic search capabilities allow for context-aware memory retrieval, going beyond simple keyword matching.

### Automatic Categorization

MEM0 automatically categorizes memories based on content, making organization more efficient.

### Relevance Scoring

MEM0 ranks memories by relevance to the current context, ensuring the most important information is prioritized.

### Long-Term Memory Optimization

MEM0 optimizes memory storage and retrieval for long-term use, preventing degradation over time.

## Fallback Mechanism

The OBJX Platform includes a local storage fallback mechanism that activates when MEM0 is unavailable. While this provides basic functionality, it lacks the advanced features of MEM0:

- Simple file-based storage instead of vector embeddings
- Keyword-based search instead of semantic search
- No automatic categorization or relevance scoring

For the full OBJX experience, ensure MEM0 is properly configured and accessible.

## Troubleshooting

### API Key Issues

If you encounter authentication errors:

1. Verify your API key is correct
2. Check that your MEM0 subscription is active
3. Ensure the API key has the necessary permissions

### Connection Issues

If the platform cannot connect to MEM0:

1. Check your internet connection
2. Verify MEM0 service status
3. Ensure firewall settings allow the connection

### Memory Not Saving

If memories aren't being saved:

1. Check that the user's tier allows memory (Tier 2 or 3)
2. Verify the correct user_id is being used
3. Check for error messages in the logs

## Support

For additional support with MEM0 integration:

- Visit the MEM0 documentation: https://docs.mem0.ai/
- Contact MEM0 support: support@mem0.ai
- Check the OBJX Platform documentation for platform-specific guidance

