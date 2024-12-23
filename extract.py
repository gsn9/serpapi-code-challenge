import json
from bs4 import BeautifulSoup

def load_html(file_path):
    """
    Load the HTML content from the provided file path and return a BeautifulSoup object.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return BeautifulSoup(file.read(), 'html.parser')
    except FileNotFoundError:
        raise Exception(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"An error occurred while loading the HTML: {e}")

def extract_paintings(soup):
    """
    Extract painting information (name, extensions, link, thumbnail) from the given BeautifulSoup object.

    Returns:
        list: A list of dictionaries, each containing painting details.
    """
    paintings = []
    try:
        carousel = soup.find('g-scrolling-carousel')  # Locate the carousel
        if not carousel:
            print("No carousel found in the HTML.")
            return paintings

        # Each painting card is an anchor with class "klitem"
        items = carousel.select('a.klitem')
        for item in items:
            try:
                name_tag = item.find('div', class_='kltat')
                extensions_tag = item.find('div', class_='klmeta')
                link_tag = item.get('href')
                img_tag = item.select_one('.klic img.rISBZc')

                # Extract name
                name = name_tag.get_text(strip=True) if name_tag else None

                # Extract extensions (year, etc.)
                extensions = extensions_tag.get_text(strip=True).split(', ') if extensions_tag else []

                # Construct the full link
                link = f"https://www.google.com{link_tag}" if link_tag else None

                # Extract thumbnail
                thumbnail = img_tag.get('data-src') or img_tag.get('src') if img_tag else None

                # Only add if we have a valid name and link
                if name and link:
                  paintings.append({
                      'name': name,
                      'extensions': extensions,
                      'link': link,
                      'thumbnail': thumbnail
                  })
            except Exception as e:
                print(f"Error processing item: {e}")
    except Exception as e:
        raise Exception(f"An error occurred during extraction: {e}")
    return paintings

def save_as_json(data, output_path):
    """
    Save the given data to a JSON file.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(f"Extracted data saved to {output_path}")
    except Exception as e:
        raise Exception(f"An error occurred while saving to JSON: {e}")

def main():
    input_file = 'C:\\code_repos\\serpapi\\serpapi-code-challenge\\files\\van-gogh-paintings.html'
    output_file = 'python_extracted_paintings.json'

    try:
        soup = load_html(input_file)
        paintings = extract_paintings(soup)
        save_as_json(paintings, output_file)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
