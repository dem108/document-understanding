# convert PDFs to images

def convert_pdf_to_images(pdf_file, prefix, image_dir):
    from pdf2image import convert_from_path
    from PIL import Image
    import os
    import shutil

    # create image directory if it doesn't exist
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # convert pdf to images
    images = convert_from_path(pdf_file, dpi=300)

    # save images to image directory
    for i, image in enumerate(images):
        image.save(image_dir + '\\' + prefix + '_' + str(i) + '.jpg', 'JPEG')

if __name__ == "__main__":
    import os
    script_path = os.path.dirname(__file__)

    target_files_path = os.path.join(script_path, "..", "target_files.3.txt")
    # target_files_path = os.path.join(script_path, "..", "target_files.sample-doc1.txt")
    # target_files_path = os.path.join(script_path, "..", "target_files.sample-doc.txt")
    # target_files_path = os.path.join(script_path, "..", "target_files.txt")
    # target_files_path = os.path.join(script_path, "..", "target_files.real-doc.txt")
    # target_files_path = os.path.join(script_path, "..", "target_files.real-all.txt")

    with open(target_files_path, "r", encoding='utf-8-sig') as f_target:
        str_path_to_files = f_target.read().splitlines()

        for path_to_file in str_path_to_files:
            # only process PDF files
            if path_to_file.lower().endswith(".pdf"):
                # get the name of the file without the extension
                print("Processing: {}".format(path_to_file))
                # get the directory name to save images under the same directory as the PDF file
                image_dir = os.path.dirname(path_to_file)
                # get the file name without the extension
                file_name = os.path.splitext(os.path.basename(path_to_file))[0]
                # convert the PDF to images
                convert_pdf_to_images(path_to_file, file_name, image_dir)

