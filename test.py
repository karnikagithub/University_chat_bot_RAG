import os
if not os.path.exists('faiss_index'):
    os.makedirs('faiss_index')


# import os

# index_file_path = r"D:\University_Bot\University_Bot_faiss\faiss_index\index.faiss"
# if os.path.exists(index_file_path):
#     print("File found!")
# else:
#     print("File not found!")

# List all available models



import faiss
import numpy as np

# Example data (100 vectors of 128 dimensions)
vectors = np.random.rand(100, 128).astype('float32')

# Create a FAISS index
index = faiss.IndexFlatL2(128)  # Using a basic index for simplicity
index.add(vectors)

# Save the index to a file
faiss.write_index(index, r"D:\University_Bot\University_Bot_faiss\faiss_index\index.faiss")