import unittest
from bs4 import BeautifulSoup
from extract import load_html, extract_paintings

class TestExtractPaintings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Load the test HTML file once for all tests.
        """
        cls.test_html_path = 'C:\\code_repos\\serpapi\\serpapi-code-challenge\\files\\van-gogh-paintings.html'
        cls.invalid_html_path = 'nonexistent_file.html'  # For error testing
        with open(cls.test_html_path, 'r', encoding='utf-8') as file:
            cls.html_content = file.read()
        cls.soup = BeautifulSoup(cls.html_content, 'html.parser')

    # Happy tests
    def test_load_html(self):
        """
        Test the load_html function with valid input.
        """
        soup = load_html(self.test_html_path)
        self.assertIsInstance(soup, BeautifulSoup)

    def test_extract_paintings(self):
        """
        Test the extract_paintings function with a valid HTML.
        """
        paintings = extract_paintings(self.soup)

        # Ensure we have a non-empty result
        self.assertGreater(len(paintings), 0, "No paintings extracted.")

        # Check structure of the first painting
        painting = paintings[0]
        self.assertIn('name', painting)
        self.assertIn('extensions', painting)
        self.assertIn('link', painting)
        self.assertIn('thumbnail', painting)

    def test_no_carousel(self):
        """
        Test extract_paintings when no carousel is present in the HTML.
        """
        soup = BeautifulSoup("<html></html>", 'html.parser')  # Empty HTML
        paintings = extract_paintings(soup)
        self.assertEqual(len(paintings), 0, "Should return an empty list when no carousel is present.")

    # Unhappy tests
    def test_load_html_file_not_found(self):
      """
      Test load_html with a non-existent file.
      """
      with self.assertRaises(Exception) as context:
          load_html(self.invalid_html_path)
      self.assertIn("File not found", str(context.exception))


    def test_extract_paintings_missing_fields(self):
        """
        Test extract_paintings when some fields are missing.
        """
        soup = BeautifulSoup("<g-scrolling-carousel><a class='klitem'></a></g-scrolling-carousel>", 'html.parser')
        paintings = extract_paintings(soup)
        self.assertEqual(len(paintings), 0, "Should not extract paintings when fields are missing.")



    def test_extract_paintings_invalid_html(self):
        """
        Test extract_paintings with completely invalid HTML.
        """
        soup = BeautifulSoup("<invalid><html>", 'html.parser')
        paintings = extract_paintings(soup)
        self.assertEqual(len(paintings), 0, "Should return an empty list for invalid HTML.")

if __name__ == "__main__":
    unittest.main()
