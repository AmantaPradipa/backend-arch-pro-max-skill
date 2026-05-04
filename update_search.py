import re
from pathlib import Path

def update_search_script(path_str):
    path = Path(path_str)
    if not path.exists():
        return
        
    content = path.read_text(encoding='utf-8')
    
    # 1. Update CSV_CONFIG
    content = re.sub(
        r'("output_cols":\s*\[)(.*?)("references")(\],?)',
        r'\1\2\3, "source_url", "source_type", "last_updated"\4',
        content
    )
    # same for anti-patterns
    content = re.sub(
        r'("output_cols":\s*\[)(.*?)("good_example",\s*"references")(\],?)',
        r'\1\2\3, "source_url", "source_type", "last_updated"\4',
        content
    )
    
    # update STACK config columns
    content = content.replace(
        'output_cols = ["stack", "category", "guideline", "do", "dont", "notes"]',
        'output_cols = ["stack", "category", "guideline", "do", "dont", "notes", "source_url", "source_type", "last_updated"]'
    )
    
    # 2. Update search_csv
    search_csv_old = '''    for index, score in ranked[:max_results]:
        if score > 0:
            row = rows[index]
            results.append({col: row.get(col, "") for col in output_cols if col in row})
    if not results and rows:
        for row in rows[:max_results]:
            results.append({col: row.get(col, "") for col in output_cols if col in row})'''
    
    search_csv_new = '''    for index, score in ranked[:max_results]:
        if score > 0:
            row = rows[index]
            res = {col: row.get(col, "") for col in output_cols if col in row}
            res["_score"] = round(score, 2)
            if score > 5.0:
                res["_confidence"] = "high"
            elif score >= 2.0:
                res["_confidence"] = "medium"
            else:
                res["_confidence"] = "low"
            results.append(res)
    if not results and rows:
        for row in rows[:max_results]:
            res = {col: row.get(col, "") for col in output_cols if col in row}
            res["_score"] = 0.0
            res["_confidence"] = "none"
            results.append(res)'''
            
    content = content.replace(search_csv_old, search_csv_new)
    
    # 3. Update format_results
    format_results_old = '''    for index, row in enumerate(result.get("results", []), 1):
        lines.append(f"### Result {index}")
        for key, value in row.items():
            value = str(value)
            if len(value) > 360:
                value = value[:360] + "..."
            lines.append(f"- **{key}:** {value}")
        lines.append("")'''
        
    format_results_new = '''    for index, row in enumerate(result.get("results", []), 1):
        score = row.pop("_score", None)
        conf = row.pop("_confidence", None)
        title_suffix = f" (Score: {score}, Confidence: {conf})" if score is not None else ""
        lines.append(f"### Result {index}{title_suffix}")
        for key, value in row.items():
            value = str(value)
            if len(value) > 360:
                value = value[:360] + "..."
            lines.append(f"- **{key}:** {value}")
        lines.append("")'''
        
    content = content.replace(format_results_old, format_results_new)
    
    # 4. Insert Compare mode function
    compare_func = '''
def compare_items(query, domain=None):
    terms = re.split(r"(?i)\s+vs\s+", query)
    if len(terms) < 2:
        return {"error": "Compare mode requires terms separated by ' vs ', e.g., 'RabbitMQ vs Kafka'"}
    
    domain = domain or detect_domain(query)
    
    comparisons = []
    for term in terms:
        res = search(term.strip(), domain, 1)
        if res.get("results"):
            comparisons.append(res["results"][0])
        else:
            comparisons.append({"name": term.strip(), "description": "Not found in domain."})
    
    keys = []
    for comp in comparisons:
        for k in comp.keys():
            if k not in ["_score", "_confidence"] and k not in keys:
                keys.append(k)
                
    lines = [f"## Compare: {' vs '.join(t.strip() for t in terms)}"]
    
    header = "| Feature | " + " | ".join(comp.get("name", "Unknown") for comp in comparisons) + " |"
    lines.append(header)
    dash_row = "|---|" + "|".join("---" for _ in comparisons) + "|"
    lines.append(dash_row)
    
    for key in keys:
        if key == "name":
            continue
        row_str = f"| **{key.replace('_', ' ').title()}** | "
        cols = []
        for comp in comparisons:
            val = str(comp.get(key, "-")).replace("\\n", " ").replace("|", ", ")
            if len(val) > 150:
                val = val[:147] + "..."
            cols.append(val)
        row_str += " | ".join(cols) + " |"
        lines.append(row_str)
        
    return {"compare_markdown": "\\n".join(lines)}

def main():'''
    content = content.replace("def main():", compare_func)
    
    # 5. Update main()
    main_old = '''    parser = argparse.ArgumentParser(description="Backend Arch Pro Max Search")
    parser.add_argument("query", help="Search query")'''
    
    main_new = '''    if len(sys.argv) > 1 and sys.argv[1] == "compare":
        parser = argparse.ArgumentParser(description="Compare Mode")
        parser.add_argument("command", help="Command (compare)")
        parser.add_argument("query", help="Compare query, e.g. 'RabbitMQ vs Kafka'")
        parser.add_argument("--domain", "-d", choices=list(CSV_CONFIG.keys()), help="Search domain", default=None)
        args = parser.parse_args()
        
        result = compare_items(args.query, args.domain)
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(result["compare_markdown"])
        return

    parser = argparse.ArgumentParser(description="Backend Arch Pro Max Search")
    parser.add_argument("query", help="Search query")'''
    
    content = content.replace(main_old, main_new)
    
    path.write_text(content, encoding='utf-8')
    print(f"Updated {path}")

# Run updates
update_search_script('d:/Pemrograman/Agent-Skills/backend-arch-pro-max-skill/scripts/search.py')
update_search_script('d:/Pemrograman/Agent-Skills/backend-arch-pro-max-skill/cli/assets/skill/scripts/search.py')
