# VERZIJA 2DEC
import re,os


def split_bibitems(input_string):
    # Define the pattern to match \bibitem
    bibitem_pattern = re.compile(r'\\bibitem')

    # Use finditer to find the positions of \bibitem occurrences
    bibitem_positions = [match.start() for match in bibitem_pattern.finditer(input_string)]

    # Add the end position of the string to mark the end of the last block
    bibitem_positions.append(len(input_string))

    # Initialize an array to store the blocks
    blocks = []

    # Iterate through the positions to extract the blocks
    for i in range(len(bibitem_positions) - 1):
        start_pos = bibitem_positions[i]
        end_pos = bibitem_positions[i + 1]
        block = input_string[start_pos:end_pos].strip()
        blocks.append(block)

    return blocks


def extract_bibliography(content):
    # Define the pattern to match \begin{thebibliography}{999} and \end{thebibliography}
    bibliography_pattern = re.compile(r'\\begin\{thebibliography\}\{[0-9]+\}(.*?)\\end\{thebibliography\}', re.DOTALL)
    end_chunk = "\\end{thebibliography}"

    # Find the bibliography block in the content
    bibliography_match = split_bibitems(
        bibliography_pattern.search(content).group(0).replace(end_chunk, ""))
    return bibliography_match


def custom_sorting_key(item):
    key = item[0]
    return order_of_citations.index(key) if key in order_of_citations else len(order_of_citations)


##########################################


file_path = [file for file in os.listdir() if 'done' in file.lower() and '.tex' in file.lower()][0]


with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

    order_of_citations = [item.strip() for item in content.splitlines()[0].replace('%', '').split(',')]

    Chicago_type = True if content.splitlines()[0] == "%Chicago" else False

    bibliography = extract_bibliography(content)

    pattern = re.compile(r'bibitem(?:\[[^\]]+\])?{([^}]+)}')
    #pattern2 = re.compile(r'bibitem(?:\[[^\]]+\])?{([^}]+)}')

    bibliographyDict = {}

    for string in bibliography:

        match = pattern.search(string)
        #match2 = pattern2.search(string)
        if match: # or match2:
            if Chicago_type:
                key = string.splitlines()[1]
                bibliographyDict[key] = string
            else:
                key = match.group(1) #if match is not None else match2.group(1)  # Extract content within the curly braces
                bibliographyDict[key] = string

    print(bibliographyDict)

    # Sort the dictionary based on the custom sorting key
    if content.splitlines()[0] == "%Chicago":
        sorted_items = sorted(bibliographyDict.items(), key=lambda i: i[0].lower())
    else:
        sorted_items = sorted(bibliographyDict.items(), key=custom_sorting_key)

    # Create a new dictionary from the sorted items
    sorted_dict = dict(sorted_items)

    with open(file_path.replace(".tex", "")+'_reordered_references.tex', 'a', encoding='utf-8') as file:
        for value in sorted_dict.values():
            file.write(value+'\n\n')





