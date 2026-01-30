def analyze_repo(repo, llm_handler=None):
    """
    Analyzes the repository for language, potential security vulnerabilities, and existing workflows.
    Uses LLM for deeper analysis if handler is provided.
    """
    analysis = {}
    
    # 1. Programming Language
    analysis['language'] = repo.language
    
    # 2. Potential Security Vulnerabilities
    vulnerabilities = []
    file_contents = {}
    
    try:
        contents = repo.get_contents("")
        # Simple heuristic: grab specific files for LLM analysis
        files_to_scan = [f for f in contents if f.name.endswith('.py') or f.name.endswith('.js') or f.name == 'README.md']
        # Limit to first 3 to avoid token limits in this demo
        for f in files_to_scan[:3]:
            try:
                decoded = f.decoded_content.decode('utf-8')
                file_contents[f.name] = decoded
            except:
                pass
                
        if llm_handler and file_contents:
            print("Sending files to LLM for analysis...")
            llm_analysis = llm_handler.analyze_codebase(file_contents)
            vulnerabilities.append(f"LLM Analysis:\n{llm_analysis}")
        else:
             # Fallback to basic check
            for content_file in contents:
                if "password" in content_file.name.lower() or "secret" in content_file.name.lower():
                     vulnerabilities.append(f"Suspicious file name found: {content_file.name}")
    except Exception as e:
        vulnerabilities.append(f"Error scanning files: {e}")
        
    analysis['vulnerabilities'] = vulnerabilities if vulnerabilities else ["No obvious issues found."]

    # 3. Existing Workflows
    workflows = []
    try:
        wf_contents = repo.get_contents(".github/workflows")
        for wf in wf_contents:
            workflows.append(wf.name)
    except:
        workflows.append("No .github/workflows directory found.")
        
    analysis['workflows'] = workflows
    
    return analysis
