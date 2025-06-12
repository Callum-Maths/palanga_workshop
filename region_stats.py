import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_parquet('part-00000-c0fa7496-921d-48fd-88e8-33ac5109cff7-c000.snappy.parquet')

total_value_vector = df['total_value_of_services'].values
fmf_value_vector = df['fmf_value'].values
region_vector = df['customer_municipality'].values
age_vector = df['customer_age_group'].values
tenure_vector = df['customer_tenure'].values

def region_stats(region):
    region_mask = region_vector == region
    total_value = total_value_vector[region_mask]
    fmf_value = fmf_value_vector[region_mask]
    age = age_vector[region_mask]
    tenure = tenure_vector[region_mask]

    if len(total_value) == 0:
        return None

    stats = {
        'region': region,
        'total_value_mean': total_value.mean(),
        'total_value_std': total_value.std(),
        'fmf_value_mean': fmf_value.mean(),
        'fmf_value_std': fmf_value.std(),
    }
    
    return stats

unique_regions = df['customer_municipality'].unique()

# Filter out None values
valid_regions = []
valid_total_means = []
valid_fmf_means = []

for i, region in enumerate(unique_regions):
    if region is not None and not pd.isna(region):
        stats = region_stats(region)
        if stats is not None:
            valid_regions.append(region)
            valid_total_means.append(stats['total_value_mean'])
            valid_fmf_means.append(stats['fmf_value_mean'])

# Join the three vectors into a 3 x N matrix
region_stats_matrix = np.vstack([valid_regions, valid_total_means, valid_fmf_means])

# Split regions into "miesto" and "rajona"
miesto_indices = [i for i, r in enumerate(valid_regions) if 'miesto' in str(r).lower()]
rajono_indices = [i for i, r in enumerate(valid_regions) if 'rajono' in str(r).lower()]
misc_indices = [i for i, r in enumerate(valid_regions) if 'miesto' not in str(r).lower() and 'rajono' not in str(r).lower()]

print("Rajono indices:", rajono_indices)
print("Miesto indices:", miesto_indices)

miesto_regions = [valid_regions[i] for i in miesto_indices]
miesto_total_means = [valid_total_means[i] for i in miesto_indices]
miesto_fmf_means = [valid_fmf_means[i] for i in miesto_indices]

rajono_regions = [valid_regions[i] for i in rajono_indices]
rajono_total_means = [valid_total_means[i] for i in rajono_indices]
rajono_fmf_means = [valid_fmf_means[i] for i in rajono_indices]

misc_regions = [valid_regions[i] for i in misc_indices]
misc_total_means = [valid_total_means[i] for i in misc_indices]
misc_fmf_means = [valid_fmf_means[i] for i in misc_indices]

print("Miesto regions:", miesto_regions)
print("Rajono regions:", rajono_regions)
print("Misc regions:", misc_regions)

# Update the plotting code to use the filtered data
plt.figure(figsize=(12, 6))
plt.bar(miesto_regions, miesto_total_means, label='Total Value Mean (Miesto)', alpha=0.6, color='blue')
plt.bar(miesto_regions, miesto_fmf_means, label='FMF Value Mean (Miesto)', alpha=0.6 , color='orange')
plt.bar(rajono_regions, rajono_total_means, label='Total Value Mean (Rajono)', alpha=0.6, color='green')
plt.bar(rajono_regions, rajono_fmf_means, label='FMF Value Mean (Rajono)', alpha=0.6, color='red')
plt.bar(misc_regions, misc_total_means, label='Total Value Mean (Misc)', alpha=0.6, color='purple')
plt.bar(misc_regions, misc_fmf_means, label='FMF Value Mean (Misc)', alpha=0.6, color='pink')
plt.xlabel('Region')
plt.ylabel('Mean Value')
plt.title('Mean Values by Region')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig('region_vs_spendature6.png')

    