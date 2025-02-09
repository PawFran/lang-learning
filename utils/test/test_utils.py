import pytest
from utils.lib.utils import process_text  # Import the function to be tested


@pytest.mark.parametrize(
    "input_text, expected_words, expected_example, expected_context",
    [
        # Test case 1: Single word outside brackets
        (
            "spotty (Thanks to the wifi... which is \\spotty\\ at best) [The simpsons - Lisa]",
            {"spotty"},
            "Thanks to the wifi... which is spotty at best",
            "The simpsons - Lisa"
        ),

        # Test case 2: Multiple words outside brackets + escaped words inside parentheses
        (
            "indolent (I began to \\indolently\\ study \\diseases\\, generally) [Three Men in a Boat (to say nothing of the dog)]",
            {"indolent", "indolently", "diseases"},
            "I began to indolently study diseases, generally",
            "Three Men in a Boat (to say nothing of the dog)"
        ),

        # Test case 3: No words outside brackets, but words in []
        (
            "(Some text here) [Example with \\word1\\ and \\word2\\ inside]",
            {"word1", "word2"},
            "Some text here",
            "Example with word1 and word2 inside"
        ),

        # Test case 4: No parentheses, only words outside brackets
        (
            "Simple text without brackets at all",
            {"Simple", "text", "without", "brackets", "at", "all"},
            "",
            ""
        ),

        # Test case 5: Empty input
        (
            "",
            set(),
            "",
            ""
        ),

        # Test case 6: No words outside brackets, no words in []
        (
            "(Only example text) [Only context text]",
            set(),
            "Only example text",
            "Only context text"
        ),

        # Test case 7: Words inside () but not escaped -> should NOT be added to words
        (
            "random (some \\word_inside\\ text here) [Context with \\another_word\\]",
            {"random", "word_inside", "another_word"},
            "some word_inside text here",
            "Context with another_word"
        ),
    ]
)


def test_process_text(input_text, expected_words, expected_example, expected_context):
    words, example, context = process_text(input_text)
    
    assert words == expected_words, f"Expected words: {expected_words}, but got: {words}"
    assert example == expected_example, f"Expected example: {expected_example}, but got: {example}"
    assert context == expected_context, f"Expected context: {expected_context}, but got: {context}"
