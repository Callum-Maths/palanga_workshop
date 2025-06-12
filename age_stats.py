import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_parquet('part-00000-c0fa7496-921d-48fd-88e8-33ac5109cff7-c000.snappy.parquet')

total_value_vector = df['total_value_of_services'].values
fmf_value_vector = df['fmf_value'].values
region_vector = df['customer_municipality'].values
age_vector = df['customer_age_group'].values
tenure_vector = df['customer_tenure'].values

def age_stats(age):
    age_mask = age_vector == age
    total_value = total_value_vector[age_mask]
    fmf_value = fmf_value_vector[age_mask]
    age = age_vector[age_mask]
    tenure = tenure_vector[age_mask]

    if len(total_value) == 0:
        return None

    stats = {
        'age': age,
        'total_value_mean': total_value.mean(),
        'total_value_std': total_value.std(),
        'fmf_value_mean': fmf_value.mean(),
        'fmf_value_std': fmf_value.std(),
    }
    
    return stats

unique_ages = df['customer_age_group'].unique()
# Filter out None values
valid_ages = []
valid_total_means = []
valid_fmf_means = []
valid_fmf_stds = []

for i, age in enumerate(unique_ages):
    if age is not None and not pd.isna(age):
        stats = age_stats(age)
        if stats is not None:
            valid_ages.append(age)
            valid_total_means.append(stats['total_value_mean'])
            valid_fmf_means.append(stats['fmf_value_mean'])

# Join the three vectors into a 3 x N matrix
# Convert valid_ages to strings and sort indices by the first digit
sorted_indices = sorted(range(len(valid_ages)), key=lambda i: str(valid_ages[i])[0])
valid_ages = [valid_ages[i] for i in sorted_indices]
valid_total_means = [valid_total_means[i] for i in sorted_indices]
valid_fmf_means = [valid_fmf_means[i] for i in sorted_indices]

age_stats_matrix = np.vstack([valid_ages, valid_total_means, valid_fmf_means])

# Plotting the age statistics
plt.figure(figsize=(12, 6))
plt.bar(valid_ages, valid_total_means, label='Total Value Mean', alpha=0.6)
plt.bar(valid_ages, valid_fmf_means, label='FMF Value Mean', alpha=0.6)
plt.xlabel('Age Group')
plt.ylabel('Mean Value')
plt.title('Age Group Statistics')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig('age_group_statistics.png')
