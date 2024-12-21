require 'nokogiri'
require 'json'

# Load the HTML content from the provided file path and return a Nokogiri object.
def load_html(file_path)
  begin
    File.open(file_path, 'r:utf-8') do |file|
      return Nokogiri::HTML(file.read)
    end
  rescue Errno::ENOENT
    raise "File not found: #{file_path}"
  rescue StandardError => e
    raise "An error occurred while loading the HTML: #{e}"
  end
end

# Extract painting information (name, extensions, link, thumbnail) from the given Nokogiri object.
def extract_paintings(doc)
  paintings = []

  begin
    carousel = doc.at('g-scrolling-carousel') # Locate the carousel
    unless carousel
      puts "No carousel found in the HTML."
      return paintings
    end

    # Each painting card is an anchor with class "klitem"
    items = carousel.css('a.klitem')

    items.each do |item|
      begin
        name_tag = item.at('div.kltat')
        extensions_tag = item.at('div.klmeta')
        link_tag = item['href']
        img_tag = item.at('.klic img.rISBZc')

        # Extract name
        name = name_tag&.text&.strip

        # Extract extensions (year, etc.)
        extensions = extensions_tag&.text&.strip&.split(', ')

        # Construct the full link
        link = link_tag ? "https://www.google.com#{link_tag}" : nil

        # Extract thumbnail
        thumbnail = img_tag&.[]('data-src') || img_tag&.[]('src')

        # Only add if we have a valid name and link
        if name && link
          paintings << {
            name: name,
            extensions: extensions || [],
            link: link,
            thumbnail: thumbnail
          }
        end
      rescue StandardError => e
        puts "Error processing item: #{e}"
      end
    end
  rescue StandardError => e
    raise "An error occurred during extraction: #{e}"
  end

  paintings
end

# Save the given data to a JSON file.
def save_as_json(data, output_path)
  begin
    File.open(output_path, 'w:utf-8') do |file|
      file.write(JSON.pretty_generate(data))
    end
    puts "Extracted data saved to #{output_path}"
  rescue StandardError => e
    raise "An error occurred while saving to JSON: #{e}"
  end
end

# Main function to load, extract, and save the paintings data.
def main
  input_file = 'C:\\code_repos\\serpapi\\serpapi-code-challenge\\files\\van-gogh-paintings.html'
  output_file = 'ruby_extracted_paintings.json'

  begin
    doc = load_html(input_file)
    paintings = extract_paintings(doc)
    save_as_json(paintings, output_file)
  rescue StandardError => e
    puts "Error: #{e}"
  end
end

# Run the main function if the script is executed directly.
if __FILE__ == $PROGRAM_NAME
  main
end
