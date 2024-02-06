# DENK-API-OCR-Python-Example

* Install the following Python packages:
  - protobuf==3.13.0
* Put the following files into the same directory as *example.py*:
  - denk.dll - From *DOWNLOADED DENK API FILES*\DENK_API_Static_OpenCV\CPU\denk.dll
  - onnxruntime.dll - From *DOWNLOADED DENK API FILES*\Dependencies\CPU\onnxruntime.dll
* Put an OCR network file from the Hub into the "models" directory
* Do either of the following in *example.py*:
  - Set the *token* variable to a machine token from the Hub
  - Plug in a USB dongle and set *use_dongle* to True
* Set a path to an image file in *example_image_file* in *example.py*
* Run the script via *python example.py*