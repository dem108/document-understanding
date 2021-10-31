# coding: utf-8

import os

def format_bounding_region(bounding_regions):
    if not bounding_regions:
        return "N/A"
    return "\"" + ", ".join("Page #{}: {}".format(region.page_number, format_bounding_box(region.bounding_box).replace("\"","")) for region in bounding_regions) + "\""

def format_bounding_box(bounding_box):
    if not bounding_box:
        return "N/A"
    return "\"" + ", ".join(["[{}, {}]".format(p.x, p.y) for p in bounding_box]) + "\""

def format_content(content):
    if not content:
        return "N/A"
    return "\"" + content.replace("\"", "") + "\""


def analyze_general_documents(path_to_documents, f_desc, f_kvp_csv, f_entity_csv, f_item_csv, f_table_csv):
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.formrecognizer import DocumentAnalysisClient

    endpoint = os.environ["AZURE_FORM_RECOGNIZER_ENDPOINT"]
    key = os.environ["AZURE_FORM_RECOGNIZER_KEY"]

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    with open(path_to_documents, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-document", document=f
        )
    result = poller.result()

    def write_desc(s):
        print("{}".format(s), file=f_desc)
    def write_kvp_csv(s):
        print("{}".format(s), file=f_kvp_csv)
    def write_entity_csv(s):
        print("{}".format(s), file=f_entity_csv)
    def write_item_csv(s):
        print("{}".format(s), file=f_item_csv)
    def write_table_csv(s):
        print("{}".format(s), file=f_table_csv)

    # Print the document file name
    write_desc("")
    write_desc("====Document file name: {}".format(path_to_documents))
    write_desc("----------------------------------------")

    # Print handwritten text
    for style in result.styles:
        if style.is_handwritten:
            write_desc("Document contains handwritten content: ")
            write_desc(",".join([result.content[span.offset:span.offset + span.length] for span in style.spans]))

    # Print key-value pairs
    write_desc("\n----Key-value pairs found in document----")
    for kv_pair in result.key_value_pairs:
        if kv_pair.key:
            write_desc(
                    "Key '{}' found within '{}' bounding regions".format(
                        kv_pair.key.content,
                        format_bounding_region(kv_pair.key.bounding_regions),
                    )
                )
        if kv_pair.value:
            write_desc(
                    "Value '{}' found within '{}' bounding regions\n".format(
                        kv_pair.value.content,
                        format_bounding_region(kv_pair.value.bounding_regions),
                    )
                )
        if kv_pair.key: # note: kv_pair.value can be None (in case only keys are extracted not values)
            write_kvp_csv(",".join([path_to_documents,
                format_content(kv_pair.key.content),
                format_content(kv_pair.value.content if kv_pair.value else ""),
                str(kv_pair.confidence),
                format_bounding_region(kv_pair.key.bounding_regions),
                (format_bounding_region(kv_pair.value.bounding_regions) if kv_pair.value else "")]))

    # Print entities
    write_desc("\n----Entities found in document----")
    for entity in result.entities:
        write_desc("Entity of category '{}' with sub-category '{}'".format(entity.category, entity.sub_category))
        write_desc("...has content '{}'".format(entity.content))
        write_desc("...within '{}' bounding regions".format(format_bounding_region(entity.bounding_regions)))
        write_desc("...with confidence {}\n".format(entity.confidence))

        # sub_category can be None
        write_entity_csv(",".join([path_to_documents, 
            entity.category, 
            (entity.sub_category if entity.sub_category else ""), 
            format_content(entity.content), 
            str(entity.confidence), 
            format_bounding_region(entity.bounding_regions)]))

    # Print all items (lines, words, selection marks)
    for page in result.pages:
        write_desc("\n----Analyzing document from page #{}----".format(page.page_number))
        write_desc(
            "Page has width: {} and height: {}, measured with unit: {}".format(
                page.width, page.height, page.unit
            )
        )

        for line_idx, line in enumerate(page.lines):
            write_desc(
                "...Line # {} has text content '{}' within bounding box '{}'".format(
                    line_idx,
                    line.content,
                    format_bounding_box(line.bounding_box),
                )
            )

            write_item_csv(",".join([path_to_documents, 
                str(page.page_number), 
                str(page.width), 
                str(page.height), 
                page.unit, 
                "line",
                format_content(line.content),
                "",
                str(line_idx),
                format_bounding_box(line.bounding_box)]))

        for word in page.words:
            write_desc(
                "...Word '{}' has a confidence of {}".format(
                    word.content, word.confidence
                )
            )

            write_item_csv(",".join([path_to_documents, 
                str(page.page_number), 
                str(page.width), 
                str(page.height), 
                page.unit, 
                "word",
                format_content(word.content),
                str(word.confidence),
                "",
                ""]))

        for selection_mark in page.selection_marks:
            write_desc(
                "...Selection mark is '{}' within bounding box '{}' and has a confidence of {}".format(
                    selection_mark.state,
                    format_bounding_box(selection_mark.bounding_box),
                    selection_mark.confidence,
                )
            )

            write_item_csv(",".join([path_to_documents, 
                str(page.page_number), 
                str(page.width), 
                str(page.height), 
                page.unit, 
                "selection_mark",
                format_content(selection_mark.state),
                str(selection_mark.confidence),
                "",
                format_bounding_box(selection_mark.bounding_box)]))


    # Print tables
    for table_idx, table in enumerate(result.tables):
        table_region_page_number = 0
        table_region_bb = ""
        cell_region_page_number = 0
        cell_region_bb = ""
        
        write_desc(
            "Table # {} has {} rows and {} columns".format(
                table_idx, table.row_count, table.column_count
            )
        )
        for region in table.bounding_regions:
            write_desc(
                "Table # {} location on page: {} is {}".format(
                    table_idx,
                    region.page_number,
                    format_bounding_box(region.bounding_box),
                )
            )
            table_region_page_number = region.page_number
            table_region_bb = region.bounding_box
            # If we have more than one (table) region, this will be the last one.

        for cell in table.cells:
            write_desc(
                "...Cell[{}][{}] has content '{}'".format(
                    cell.row_index,
                    cell.column_index,
                    cell.content,
                )
            )
            for region in cell.bounding_regions:
                write_desc(
                    "...content on page {} is within bounding box '{}'\n".format(
                        region.page_number,
                        format_bounding_box(region.bounding_box),
                    )
                )
                cell_region_page_number = region.page_number
                cell_region_bb = region.bounding_box
                #  If we have more than one (cell) region, this will be the last one.

            write_table_csv(",".join([path_to_documents, 
                str(table_region_page_number), 
                str(table_idx), 
                str(table.row_count), 
                str(table.column_count), 
                format_bounding_box(table_region_bb),
                str(cell.row_index),
                str(cell.column_index),
                format_content(cell.content),
                format_bounding_box(cell_region_bb)]))

    write_desc("----------------------------------------")


if __name__ == "__main__":
    import os
    script_path = os.path.dirname(__file__)
    # target_files_path = os.path.join(script_path, "..", "target_files.txt")
    target_files_path = os.path.join(script_path, "..", "target_files.2.txt")
    # target_files_path = os.path.join(script_path, "..", "target_files.3.txt")

    with open(target_files_path, "r", encoding='utf-8-sig') as f_target:
        str_path_to_files = f_target.read().splitlines()

    # Note on encoding: utf-8-sig allow Excel to read the file correctly. Notepad may not.
    with open(os.path.join(script_path, "results", "result.txt"), "a", encoding='utf-8-sig') as f_desc, \
        open(os.path.join(script_path, "results", "result_kvp.csv"), "a", encoding='utf-8-sig') as f_kvp_csv, \
        open(os.path.join(script_path, "results", "result_entity.csv"), "a", encoding='utf-8-sig') as f_entity_csv, \
        open(os.path.join(script_path, "results", "result_item.csv"), "a", encoding='utf-8-sig') as f_item_csv, \
        open(os.path.join(script_path, "results", "result_table.csv"), "a", encoding='utf-8-sig') as f_table_csv:

        # Write headers
        print(",".join(["document_name", "key", "value", "confidence", "key_bb", "value_bb", "human_eval"]), file=f_kvp_csv)
        print(",".join(["document_name", "category", "sub-category", "content", "confidence", "bb", "human_eval"]), file=f_entity_csv)
        print(",".join(["document_name", "page_number", "page_width", "page_height", "page_unit", "item_type", "item_content", "confidence", "line_idx", "bb", "human_eval"]), file=f_item_csv)
        print(",".join(["document_name", "page_number", "table_idx", "table_row_count", "table_column_count", "table_bb", "row_idx", "column_idx", "cell_content", "cell_bb", "human_eval"]), file=f_table_csv)

        for path_to_file in str_path_to_files:
            print("Processing: {}".format(path_to_file))
            analyze_general_documents(os.path.normpath(path_to_file), f_desc, f_kvp_csv, f_entity_csv, f_item_csv, f_table_csv)
