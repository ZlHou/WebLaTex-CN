import os
import re
import argparse
from pathlib import Path

def clean_tex_content(content):
    """
    Remove LaTeX commands and comments to extract countable text.
    """
    # 1. Remove comments
    content = re.sub(r'%.*', '', content)
    
    # 2. Remove specific environments that shouldn't be counted
    content = re.sub(r'\\\[.*?\\\]', '', content, flags=re.DOTALL)
    content = re.sub(r'\$\$.*?\$\$', '', content, flags=re.DOTALL)
    content = re.sub(r'\$.*?\$', '', content)

    # 3. Remove commands
    ignored_commands = [
        'cite', 'ref', 'label', 'usepackage', 'input', 'include', 
        'bibliography', 'bibliographystyle', 'documentclass', 'pagestyle',
        'thispagestyle', 'vskip', 'vspace', 'hspace', 'setlength', 'setcounter'
    ]
    for cmd in ignored_commands:
        content = re.sub(r'\\' + cmd + r'\{[^}]*\}', '', content)
        
    content = re.sub(r'\\[a-zA-Z]+', ' ', content)
    content = content.replace('{', ' ').replace('}', ' ')
    
    return content

def count_words_in_content(content):
    cleaned_content = clean_tex_content(content)
    
    # Count Chinese characters
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', cleaned_content)
    num_chinese = len(chinese_chars)
    
    # Count English words
    content_no_chinese = re.sub(r'[\u4e00-\u9fff]', ' ', cleaned_content)
    content_no_punct = re.sub(r'[^\w\s]', '', content_no_chinese)
    english_words = content_no_punct.split()
    num_english = len(english_words)
    
    return num_chinese, num_english

def resolve_path(base_path, input_path):
    """
    Resolve the input path relative to the project root or base path.
    """
    # Handle missing extension
    if not input_path.endswith('.tex'):
        input_path += '.tex'
        
    # 1. Check if it exists relative to CWD (Project Root)
    p_cwd = Path(input_path)
    if p_cwd.exists():
        return p_cwd
        
    # 2. Check if it exists relative to the parent file
    if base_path:
        p_rel = base_path.parent / input_path
        if p_rel.exists():
            return p_rel
            
    return p_cwd # Return the path even if it doesn't exist, to report error later

def process_file(file_path, processed_files):
    """
    Recursively process a file and its inputs, returning a tree structure.
    """
    file_path = Path(file_path)
    resolved_path = file_path.resolve()
    
    # Avoid infinite loops
    if resolved_path in processed_files:
        return None
    
    if not file_path.exists():
        return {'path': str(file_path), 'cn': 0, 'en': 0, 'total': 0, 'error': 'File not found', 'children': []}

    processed_files.add(resolved_path)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {'path': str(file_path), 'cn': 0, 'en': 0, 'total': 0, 'error': str(e), 'children': []}

    # Find inputs BEFORE cleaning
    content_no_comments = re.sub(r'%.*', '', content)
    inputs = re.findall(r'\\(?:input|include)\{([^}]+)\}', content_no_comments)
    
    # Count in current file
    cn, en = count_words_in_content(content)
    
    node = {
        'path': str(file_path),
        'cn': cn,
        'en': en,
        'total': cn + en,
        'children': []
    }
    
    # Process inputs
    for inp in inputs:
        child_path = resolve_path(file_path, inp)
        child_node = process_file(child_path, processed_files)
        if child_node:
            node['children'].append(child_node)
        
    return node

def print_tree(node, prefix="", is_last=True, current_depth=0, max_depth=None):
    if not node:
        return
        
    # Prepare the line to print
    connector = "└── " if is_last else "├── "
    
    # Calculate stats string
    stats = f"(CN: {node['cn']}, EN: {node['en']}, Total: {node['total']})"
    if 'error' in node:
        stats += f" [Error: {node['error']}]"
        
    print(f"{prefix}{connector}{node['path']} {stats}")
    
    # Check depth limit
    if max_depth is not None and current_depth >= max_depth:
        return

    # Prepare prefix for children
    child_prefix = prefix + ("    " if is_last else "│   ")
    
    # Print children
    children = node['children']
    for i, child in enumerate(children):
        print_tree(child, child_prefix, i == len(children) - 1, current_depth + 1, max_depth)

def calculate_total_stats(node):
    """
    Calculate total stats for the tree recursively.
    """
    total_cn = node['cn']
    total_en = node['en']
    
    for child in node['children']:
        c_cn, c_en = calculate_total_stats(child)
        total_cn += c_cn
        total_en += c_en
        
    return total_cn, total_en

def main():
    parser = argparse.ArgumentParser(description="Count words in LaTeX project.")
    parser.add_argument('root_file', nargs='?', default='body/graduate/content.tex', help="Root TeX file to start counting from.")
    parser.add_argument('--max-depth', type=int, default=None, help="Maximum depth of the tree to display.")
    args = parser.parse_args()
    
    root_file = Path(args.root_file)
    
    if not root_file.exists():
        # Try prepending body/graduate if user just gave filename
        alt_path = Path('body/graduate') / root_file
        if alt_path.exists():
            root_file = alt_path
        else:
            print(f"Error: Root file {root_file} not found.")
            return

    processed_files = set()
    root_node = process_file(root_file, processed_files)
    
    print("Word Count Tree Structure:")
    # Special handling for root to avoid the connector
    stats = f"(CN: {root_node['cn']}, EN: {root_node['en']}, Total: {root_node['total']})"
    print(f"{root_node['path']} {stats}")
    
    children = root_node['children']
    for i, child in enumerate(children):
        print_tree(child, "", i == len(children) - 1, current_depth=1, max_depth=args.max_depth)
        
    total_cn, total_en = calculate_total_stats(root_node)
    print("-" * 60)
    print(f"GRAND TOTAL: CN: {total_cn}, EN: {total_en}, Total: {total_cn + total_en}")

if __name__ == "__main__":
    main()
