import os
import time
import ctypes
import struct
import results_pb2


use_dongle = False # False: Use a token (see "token" below), True: Use a USB-Dongle that is plugged into the system
token = ""

example_image_file = ""


# This function prints the returned integer value in hexadecimal
def print_formatted_return(function_name, retval, t = None):
  code = struct.pack('>i', retval).hex().upper()
  if t == None:
    print(function_name + " returned: " + code)
  else:
    print(function_name + " returned: " + code + " ({} s)".format(round(t, 4)))
  if code != "DE000000":
      exit()


# Add the current working directoy to the DLL search path
os.add_dll_directory(os.getcwd())

# Load the DLL
libdll = ctypes.cdll.LoadLibrary("denk.dll")

if use_dongle:
  retval = libdll.FindDongle()
  print_formatted_return("FindDongle", retval)
else:
  retval = libdll.TokenLogin(token.encode('utf-8'), b'\x00')
  print_formatted_return("TokenLogin", retval)

# Allocate a buffer for the model information
modelinfo = b'\x00' * 10000
modelinfo_size = ctypes.c_int(len(modelinfo))

# Read all model files in the "models" directory, write the model info into "buffer" (will be ignored in this example), select the CPU (-1) as the evaluation device
retval = libdll.ReadAllModels(b'models', modelinfo, ctypes.byref(modelinfo_size), -1)
print_formatted_return("ReadAllModels", retval)

# Open the image file in the "read bytes" mode and read the data
with open(example_image_file, 'rb') as file:
    img_data = file.read()

# Allocate the variable for the dataset index
index = ctypes.c_int(0)

# Load the image data
retval = libdll.LoadImageData(ctypes.byref(index), img_data, len(img_data))
print_formatted_return("LoadImageData", retval)

# Evaluate the image
t1 = time.time()
retval = libdll.EvaluateImage(index)
t2 = time.time()
print_formatted_return("EvaluateImage", retval, t2 - t1)

# Allocate a buffer for the results of the evaluation
results = b'\x00' * 100000
results_size = ctypes.c_int(len(results))

# Get the results of the evaluation
retval = libdll.GetResults(index, results, ctypes.byref(results_size))
print_formatted_return("GetResults", retval)

# Parse the results
results_proto = results_pb2.Results()
results_proto.ParseFromString(results[:results_size.value])

# Properly end the session
retval = libdll.EndSession()
print_formatted_return("EndSession", retval)


allowed_characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Print the results
print()
for otpt in results_proto.output:
  for ftr in otpt.feature:
    print("Text: {}".format(ftr.label))
    
    # Filter by allowed characters
    filtered_text = ""
    for position in ftr.ocr_character_position:
      for ocr_character in position.ocr_character:
        # Characters are sorted by probability and this takes the first (and therefore most likely) character that is contained in allowed_characters
        if ocr_character.character in allowed_characters:
          filtered_text += ocr_character.character
          break
    print("Filtered Text: {}".format(filtered_text))