
import os
import shutil
import argparse

def copy_images_only(src_folder, dest_folder):
    # Ensure destination folders exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Define the 'images' subfolder to process
    src_subfolder = os.path.join(src_folder, 'images')
    dest_subfolder = os.path.join(dest_folder, 'images')

    # Create destination subfolder if it doesn't exist
    if not os.path.exists(dest_subfolder):
        os.makedirs(dest_subfolder)

    # Copy only .jpg files from the 'images' subfolder
    for file_name in os.listdir(src_subfolder):
        if file_name.endswith('.jpg'):
            src_file = os.path.join(src_subfolder, file_name)
            dest_file = os.path.join(dest_subfolder, file_name)
            shutil.copy2(src_file, dest_file)  # Copy file with metadata

def main():
    parser = argparse.ArgumentParser(description='Copy image files excluding JSON files.')
    parser.add_argument('src_main_folder', type=str, help='Path to the source main folder')
    args = parser.parse_args()

    src_main_folder = args.src_main_folder
    dest_main_folder = 'simclr_dataset'  # Specify your destination folder here

    copy_images_only(src_main_folder, dest_main_folder)

if __name__ == '__main__':
    main()
