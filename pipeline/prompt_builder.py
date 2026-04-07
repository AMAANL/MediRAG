def build_prompt(user_query: str, patient_context: str, ranked_chunks: list):
    """
    Builds the complete prompt with system instructions and injected context.
    """
    system_prompt = (
        "You are a clinical decision support assistant. "
        "Only use the provided medical context to answer. "
        "Always cite the source for every claim you make. "
        "Structure your response as: \n"
        "1) Possible Diagnoses (ranked by likelihood)\n"
        "2) Recommended Diagnostic Tests\n"
        "3) Treatment Considerations\n"
        "4) Sources Used\n\n"
        "Answer the user query acting as a helpful assistant using ONLY the context below."
    )
    
    context_str = "MEDICAL CONTEXT:\n\n"
    for i, chunk in enumerate(ranked_chunks):
        title = chunk['metadata'].get('title', 'Unknown Title')
        source = chunk['metadata'].get('source', 'Unknown Source')
        text = chunk['text']
        context_str += f"[SOURCE {i+1}] {title} | {source} | {text}\n\n"
        
    user_input = f"Patient Symptoms & Query: {user_query}\n"
    if patient_context.strip():
        user_input += f"Patient Context (Lab Values, Age, etc.): {patient_context}\n"
        
    return system_prompt, f"{context_str}\n\n{user_input}"
