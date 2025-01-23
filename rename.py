import os
import argparse

def rename_images(folder_path):
     try:
          files = os.listdir(folder_path)
          image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
          
          for i, file in enumerate(image_files):
               old_path = os.path.join(folder_path, file)
               file_name, extension = os.path.splitext(file)
               file_name = file_name.replace("_image", "")
               new_filename = f"{file_name}{extension}"
               new_path = os.path.join(folder_path, new_filename)

               os.rename(old_path, new_path)
               print(f"Renamed: {file} -> {new_filename}")
          
          print("Completed!!!")

     except Exception as e:
          print(f"Error : {e}")

if __name__ == '__main__':
     parser = argparse.ArgumentParser(conflict_handler='error', add_help=True, allow_abbrev=True)
     # parser.add_argument('--folder_path', type=str, required=True) # --folder_path 무조건 명시
     parser.add_argument('folder_path', type=str) # 위치 인자로 인식

     args = parser.parse_args()

     rename_images(args.folder_path)