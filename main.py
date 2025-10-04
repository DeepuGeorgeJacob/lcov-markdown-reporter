import sys
import os


def calculate_coverage(covered, total):
    """Calculates percentage and handles division by zero."""
    # Use standard rounding for coverage calculation, ensuring 100% for zero lines if total is zero.
    return (covered / total) * 100 if total > 0 else 100


def lcov_to_markdown_pure(lcov_file_path, output_file_path='coverage_summary.md'):
    """
    Reads an lcov.info file, generates a Markdown summary, and saves it to a file.

    Args:
        lcov_file_path (str): Path to the input LCOV report file.
        output_file_path (str): Path to the output Markdown summary file.
    """
    try:
        # 1. Read the LCOV file
        with open(lcov_file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        # Use GitHub Action error format for visibility in the CI log
        print(f"::error::The LCOV input file '{lcov_file_path}' was not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"::error::Error reading LCOV report '{lcov_file_path}': {e}", file=sys.stderr)
        sys.exit(1)

    # Global tracking variables
    global_metrics = {
        'lines_total': 0, 'lines_covered': 0,
        'functions_total': 0, 'functions_covered': 0,
    }

    file_breakdown = []
    current_file = None
    file_metrics = {
        'lines_total': 0, 'lines_covered': 0,
        'functions_total': 0, 'functions_covered': 0,
    }

    # 2. Parse the LCOV lines
    for line in lines:
        line = line.strip()
        # Tags are separated from data by a colon (e.g., SF:path/to/file)
        if ':' in line:
            tag, data = line.split(':', 1)
            tag = tag.strip()
            data = data.strip()
        else:
            # Skip lines without a tag/data separator (e.g., end of file marker)
            continue

        if tag == 'SF' and data:
            # SF (Source File): Start of a new file block
            if current_file:
                # Save the metrics for the previous file
                file_breakdown.append({
                    'filename': current_file,
                    **file_metrics
                })
                # Reset file metrics for the new file
                file_metrics = {k: 0 for k in file_metrics}

            current_file = data

        elif current_file:
            # Track metrics within the current file block

            if tag == 'LH':  # LH (Lines Hit) -> Lines Covered
                file_metrics['lines_covered'] = int(data)
                global_metrics['lines_covered'] += int(data)
            elif tag == 'LF':  # LF (Lines Found) -> Lines Total
                file_metrics['lines_total'] = int(data)
                global_metrics['lines_total'] += int(data)

            elif tag == 'FNF':  # FNF (Functions Found) -> Functions Total
                file_metrics['functions_total'] = int(data)
                global_metrics['functions_total'] += int(data)
            elif tag == 'FNH':  # FNH (Functions Hit) -> Functions Covered
                file_metrics['functions_covered'] = int(data)
                global_metrics['functions_covered'] += int(data)

            # Note: DA (Line Data) and FN (Function Name) are ignored for summary stats

    # Save the last file's metrics after the loop finishes
    if current_file:
        file_breakdown.append({
            'filename': current_file,
            **file_metrics
        })

    # --- 3. Global Summary Calculation ---
    overall_lines_percent = calculate_coverage(global_metrics['lines_covered'], global_metrics['lines_total'])
    overall_functions_percent = calculate_coverage(global_metrics['functions_covered'],
                                                   global_metrics['functions_total'])

    # 4. Format the data as a Markdown table

    # Global Summary
    markdown_output = "## 📊 Code Coverage Summary\n\n"
    markdown_output += "| Metric | Coverage |\n"
    markdown_output += "| :--- | :---: |\n"
    markdown_output += f"| **Lines** | **{overall_lines_percent:.2f}%** |\n"
    markdown_output += f"| **Functions** | **{overall_functions_percent:.2f}%** |\n"

    # File-by-file breakdown
    markdown_output += "\n### File Breakdown\n\n"
    markdown_output += "| File | Lines | Functions |\n"
    markdown_output += "| :--- | :---: | :---: |\n"

    for entry in file_breakdown:
        # Show just the file name (basename) for brevity in the table
        filename = os.path.basename(entry['filename'])

        lines_percent = calculate_coverage(entry['lines_covered'], entry['lines_total'])
        functions_percent = calculate_coverage(entry['functions_covered'], entry['functions_total'])

        markdown_output += f"| `{filename}` | {lines_percent:.2f}% | {functions_percent:.2f}% |\n"

    # 5. WRITE TO FILE
    try:
        with open(output_file_path, 'w') as out_f:
            out_f.write(markdown_output)
        # Output success message for the GitHub Action CI log
        print(f"::notice::Successfully generated Markdown report and saved to: {output_file_path}")
    except Exception as e:
        print(f"::error::Error writing output to file {output_file_path}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # The entrypoint.sh script passes file paths as arguments 1 and 2

    # Get input file (lcov.info) from first argument, or use a default path if run locally
    lcov_file = sys.argv[1] if len(sys.argv) > 1 else 'coverage/lcov.info'
    print(f"lcov_file path {lcov_file}")

    # Get output file (coverage_summary.md) from second argument, or use default
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'coverage_summary.md'
    print(f"output_file name {output_file}")

    lcov_to_markdown_pure(lcov_file, output_file)
