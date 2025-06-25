import argparse
import pypandoc
from bs4 import BeautifulSoup
import sys

def extract_content_html(input_file):
    """Extracts content from the target div in an HTML file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'lxml')
        content_div = soup.find('div', class_='entry-content u-text-format u-clearfix')
        if not content_div:
            raise ValueError("Could not find the specified div in the input file.")
        return str(content_div)
    except FileNotFoundError:
        sys.exit(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        sys.exit(f"An error occurred: {e}")

def convert_html_to_md(input_file, output_file):
    """Converts a specific part of an HTML file to a Markdown file."""
    print(f"Converting '{input_file}' to '{output_file}'...")
    try:
        html_content_to_convert = extract_content_html(input_file)
        markdown_content = pypandoc.convert_text(
            html_content_to_convert, 
            'md', 
            format='html',
            extra_args=['--wrap=none'] # Prevents line wrapping
        )
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print("Conversion successful!")
    except Exception as e:
        sys.exit(f"An error occurred during HTML to Markdown conversion: {e}")

def convert_md_to_html(input_file, template_file, output_file):
    """Converts a Markdown file to HTML and injects it into a template."""
    print(f"Converting '{input_file}' and injecting into '{template_file}' to create '{output_file}'...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convert Markdown to an HTML snippet
        html_snippet = pypandoc.convert_text(
            markdown_content, 
            'html', 
            format='md'
        )

        with open(template_file, 'r', encoding='utf-8') as f:
            template_html = f.read()

        soup = BeautifulSoup(template_html, 'lxml')
        content_div = soup.find('div', class_='entry-content u-text-format u-clearfix')

        if not content_div:
            raise ValueError("Could not find the target div in the template file.")

        # The converted HTML is a full document, so we need to extract the body content
        new_content_soup = BeautifulSoup(html_snippet, 'lxml')
        
        # Replace the old div's content with the new content
        content_div.replace_with(new_content_soup.find('div', class_='entry-content u-text-format u-clearfix'))

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        print("Conversion successful!")
    except FileNotFoundError as e:
        sys.exit(f"Error: File not found - {e.filename}")
    except Exception as e:
        sys.exit(f"An error occurred during Markdown to HTML conversion: {e}")


def main():
    parser = argparse.ArgumentParser(description='Convert between HTML and Markdown for specific content.')
    subparsers = parser.add_subparsers(dest='command', required=True, help='sub-command help')

    # Sub-parser for HTML to Markdown
    parser_html2md = subparsers.add_parser('html2md', help='Convert HTML content to Markdown')
    parser_html2md.add_argument('-i', '--input', required=True, help='Input HTML file path')
    parser_html2md.add_argument('-o', '--output', required=True, help='Output Markdown file path')

    # Sub-parser for Markdown to HTML
    parser_md2html = subparsers.add_parser('md2html', help='Convert Markdown to HTML and inject into a template')
    parser_md2html.add_argument('-i', '--input', required=True, help='Input Markdown file path')
    parser_md2html.add_argument('-t', '--template', required=True, help='HTML template file to inject content into')
    parser_md2html.add_argument('-o', '--output', required=True, help='Output HTML file path')

    args = parser.parse_args()

    if args.command == 'html2md':
        convert_html_to_md(args.input, args.output)
    elif args.command == 'md2html':
        convert_md_to_html(args.input, args.template, args.output)

if __name__ == '__main__':
    main() 