# import importlib.util
# import os
# import sys
#
# # Define the full path to the module file
# module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fun-mathutils-walid.py')
#
# # Create a module spec from the file location
# spec = importlib.util.spec_from_file_location("fun-mathutils-walid", '/Users/walidnewaz/.pyenv/versions/3.10.17/lib/python3.10/site-packages')
#
# # Create a new module from the spec
# my_module = importlib.util.module_from_spec(spec)
#
# # Add the module to sys.modules to make it accessible like a regular import
# sys.modules[spec.name] = my_module
#
# # Execute the module's code
# spec.loader.exec_module(my_module)

from fun_mathutils_walid import add, divide

# Now you can use the module as expected
print(add(2, 3))
print(divide(2, 3))
print(divide(5, 0))