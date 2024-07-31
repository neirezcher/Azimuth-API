import azimuth.model_comparison
import numpy as np

sequences = np.array(['ACAGCTGATCTCCAGATATGACCATGGGTT', 'CAGCTGATCTCCAGATATGACCATGGGTTT', 'CCAGAAGTTTGAGCCACAAACCCATGGTCA'])
amino_acid_cut_positions = np.array([2, 2, 4])
percent_peptides = np.array([0.18, 0.18, 0.35])
predictions = azimuth.model_comparison.predict(sequences)

for i, prediction in enumerate(predictions):
    print (sequences[i], prediction)