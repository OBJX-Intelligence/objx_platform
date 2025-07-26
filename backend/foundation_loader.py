#!/usr/bin/env python3
"""
OBJX Platform - Foundation Document Loader
Loads foundation documents for the agent system
"""

import os
import logging
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("OBJX-Foundation")

class FoundationLoader:
    """Loads and manages foundation documents"""
    
    def __init__(self, foundation_dir: str = "../foundation_docs"):
        """Initialize the foundation loader"""
        self.foundation_dir = foundation_dir
        self.documents = {}
        self.load_status = {}
        self.required_docs = [
            "00_living_doctoring_the_why.md",
            "01_foundation_principles_universal.md",
            "02_trinity_architecture_universal.md",
            "03_intelligence_memory_compound.md",
            "04_partnership_protocols_complete.md",
            "06_evolution_continuous_improvement.md"
        ]
        self.preprompt_file = "UNIVERSAL-PREPROMPT.MD"
        self.preprompt = ""
        
        # Load all foundation documents
        self.load_all_documents()
    
    def load_document(self, filename: str) -> bool:
        """Load a single foundation document"""
        filepath = os.path.join(self.foundation_dir, filename)
        
        try:
            if not os.path.exists(filepath):
                logger.warning(f"⚠️  Warning: {filename} not found in {self.foundation_dir}/")
                self.load_status[filename] = False
                return False
            
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                self.documents[filename] = content
                self.load_status[filename] = True
                return True
        except Exception as e:
            logger.error(f"❌ Error loading {filename}: {str(e)}")
            self.load_status[filename] = False
            return False
    
    def load_all_documents(self) -> Dict[str, bool]:
        """Load all foundation documents"""
        # Load required documents
        for doc in self.required_docs:
            self.load_document(doc)
        
        # Load preprompt if available
        self.load_preprompt()
        
        # Load any additional documents in the directory
        for filename in os.listdir(self.foundation_dir):
            if filename.endswith('.md') and filename not in self.documents:
                self.load_document(filename)
        
        # Log loading status
        loaded_count = sum(1 for status in self.load_status.values() if status)
        logger.info(f"📚 Foundation Documents: {loaded_count}/{len(self.required_docs)} loaded")
        
        return self.load_status
    
    def load_preprompt(self) -> bool:
        """Load the universal preprompt"""
        filepath = os.path.join(self.foundation_dir, self.preprompt_file)
        
        try:
            if not os.path.exists(filepath):
                logger.warning(f"⚠️  Warning: {self.preprompt_file} not found in {self.foundation_dir}/")
                return False
            
            with open(filepath, 'r', encoding='utf-8') as file:
                self.preprompt = file.read()
                return True
        except Exception as e:
            logger.error(f"❌ Error loading preprompt: {str(e)}")
            return False
    
    def get_document(self, filename: str) -> Optional[str]:
        """Get a specific foundation document"""
        return self.documents.get(filename)
    
    def get_all_documents(self) -> Dict[str, str]:
        """Get all loaded foundation documents"""
        return self.documents
    
    def get_preprompt(self) -> str:
        """Get the universal preprompt"""
        return self.preprompt
    
    def get_foundation_context(self) -> str:
        """Get the combined foundation context for agents"""
        context = ""
        
        # Add the preprompt first if available
        if self.preprompt:
            context += f"# UNIVERSAL PREPROMPT\n\n{self.preprompt}\n\n"
        
        # Add each foundation document in order
        for doc in self.required_docs:
            if doc in self.documents:
                doc_name = doc.replace('.md', '').replace('_', ' ').upper()
                context += f"# {doc_name}\n\n{self.documents[doc]}\n\n"
        
        return context

# Create a singleton instance
foundation_loader = None

def get_foundation_loader():
    """Get the foundation loader singleton instance"""
    global foundation_loader
    if foundation_loader is None:
        foundation_loader = FoundationLoader()
    
    return foundation_loader

# Test function
def test_foundation_loader():
    """Test the foundation loader"""
    print("Testing foundation loader...")
    
    # Get foundation loader
    loader = get_foundation_loader()
    
    # Print loading status
    print("Document loading status:")
    for doc, status in loader.load_status.items():
        print(f"  {doc}: {'✅ Loaded' if status else '❌ Not loaded'}")
    
    # Print preprompt status
    print(f"Preprompt: {'✅ Loaded' if loader.preprompt else '❌ Not loaded'}")
    
    # Print a sample of the foundation context
    context = loader.get_foundation_context()
    print(f"Foundation context length: {len(context)} characters")
    print("Sample of foundation context:")
    print(context[:500] + "...")
    
    print("Foundation loader test completed!")

if __name__ == "__main__":
    test_foundation_loader()

