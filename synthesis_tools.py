"""
Synthesis Tools - Integration wrapper for synthesis engine
"""

from synthesis_engine import SynthesisEngine
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field


# Global synthesis engine
_synthesis_engine = None
_memory_manager = None


def set_memory_manager(manager):
    """Inject memory manager from main.py"""
    global _memory_manager
    _memory_manager = manager


def get_synthesis_engine():
    """Get or create global synthesis engine"""
    global _synthesis_engine
    if _synthesis_engine is None:
        _synthesis_engine = SynthesisEngine()
    return _synthesis_engine


def synthesize_literature_wrapper(
    query: str,
    max_papers: int = 20,
    include_gaps: bool = True
) -> str:
    """
    Generate a literature review from stored papers
    
    Args:
        query: Research question (e.g., "What are attention mechanisms in deep learning?")
        max_papers: Maximum papers to analyze (default 20)
        include_gaps: Whether to identify research gaps (default True)
    
    Returns:
        Formatted literature review with citations
    """
    if _memory_manager is None:
        return "Error: Memory system not initialized"
    
    try:
        # Step 1: Search for relevant papers using hybrid search
        print(f"\n🔍 Searching for papers about: {query}")
        papers = _memory_manager.hybrid_search(
            query=query,
            top_k=max_papers,
            alpha=0.5  # Balanced keyword + semantic
        )
        
        if not papers:
            return f"No papers found for query: '{query}'. Please search and store papers first."
        
        print(f"📚 Found {len(papers)} relevant papers")
        
        # Step 2: Generate literature review
        engine = get_synthesis_engine()
        result = engine.generate_literature_review(
            papers=papers,
            query=query,
            max_papers=max_papers,
            include_gaps=include_gaps
        )
        
        if 'error' in result:
            return f"❌ Synthesis Error: {result['error']}"
        
        # Step 3: Format output
        output = f"{'='*70}\n"
        output += f"LITERATURE REVIEW: {query}\n"
        output += f"{'='*70}\n\n"
        output += result['review_text']
        output += f"\n\n{'='*70}\n"
        output += f"Analysis Statistics:\n"
        output += f"  Papers analyzed: {result['paper_count']}\n"
        output += f"  Papers cited: {len(result['citations_used'])}\n"
        output += f"  Review length: {len(result['review_text'])} characters\n"
        output += f"{'='*70}\n"
        
        return output
        
    except Exception as e:
        return f"Error in synthesis: {str(e)}"


def quick_summary_wrapper(query: str, max_papers: int = 10) -> str:
    """
    Generate a quick summary (not full review) from papers
    
    Args:
        query: Research question
        max_papers: Maximum papers to use (default 10)
    
    Returns:
        Brief summary with citations
    """
    if _memory_manager is None:
        return "Error: Memory system not initialized"
    
    try:
        # Search for papers
        papers = _memory_manager.hybrid_search(
            query=query,
            top_k=max_papers,
            alpha=0.5
        )
        
        if not papers:
            return f"No papers found for: '{query}'"
        
        # Generate quick summary
        engine = get_synthesis_engine()
        summary = engine.quick_summary(papers, query, max_length=500)
        
        return f"Quick Summary ({len(papers)} papers):\n\n{summary}"
        
    except Exception as e:
        return f"Error generating summary: {str(e)}"


# ============ TOOL SCHEMAS ============

class SynthesisArgs(BaseModel):
    query: str = Field(..., description="Research question or topic (e.g., 'What are transformer architectures?')")
    max_papers: int = Field(20, description="Maximum papers to analyze (default 20)")
    include_gaps: bool = Field(True, description="Whether to identify research gaps (default True)")


class QuickSummaryArgs(BaseModel):
    query: str = Field(..., description="Research question")
    max_papers: int = Field(10, description="Maximum papers (default 10)")


# ============ CREATE TOOLS ============

synthesis_tool = StructuredTool.from_function(
    name="generate_literature_review",
    description=(
        "Generate a structured literature review from stored papers with citation enforcement. "
        "Use this when user asks for: 'literature review', 'synthesize papers', 'what does research say about X', "
        "'summarize findings on X', 'write a review about X'. "
        "This analyzes multiple papers and generates: Introduction, Key Findings, Methodology, Research Gaps, Conclusion. "
        "Every claim is cited with [X] format. No hallucinations - only information from actual paper abstracts."
    ),
    func=synthesize_literature_wrapper,
    args_schema=SynthesisArgs,
    return_direct=False
)


quick_summary_tool = StructuredTool.from_function(
    name="quick_summary",
    description=(
        "Generate a brief summary (not full review) from papers. "
        "Use for quick answers like 'briefly tell me about X', 'quick summary of X', 'what is X in research'."
    ),
    func=quick_summary_wrapper,
    args_schema=QuickSummaryArgs,
    return_direct=False
)