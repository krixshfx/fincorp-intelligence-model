import sys
import site
import os

print(f"Executable: {sys.executable}")
print("Sys Path:")
for p in sys.path:
    print(p)

print("\nUser Site Packages:")
print(site.getusersitepackages())

try:
    import streamlit
    print("\nStreamlit imported successfully!")
    print(f"Streamlit file: {streamlit.__file__}")
except ImportError as e:
    print(f"\nFailed to import streamlit: {e}")
