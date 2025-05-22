#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Mechanical Recycling Calculator")

# User inputs
W = st.number_input("Enter the total amount of weight (kg):", min_value=0.0, value=1000.0)
R = st.slider("Enter the fraction of recycled material (0 to 1):", min_value=0.0, max_value=1.0, value=0.5)
p = st.slider("Enter the property loss per cycle (0 to 1):", min_value=0.0, max_value=1.0, value=0.2)
n = st.number_input("Enter the number of recycling cycles:", min_value=1, step=1, value=10)
l = st.slider("Enter the material loss fraction (0 to 1):", min_value=0.0, max_value=1.0, value=0.2)
T_0 = st.number_input("Enter the initial thickness:", min_value=0.0, value=1.0)
pc = 1 - p

def recycling_model(W, R, p, n, l, T_0, pc):
    property_of_raw_material = []
    thickness = []
    material_used = []
    material_collected = []
    property_of_collected = []
    recycled_material = []
    downcycled_material = []
    raw_material_saved_X1 = []
    raw_material_saved_X2 = []
    total_savings = []
    cumulative_savings = []

    property_of_raw_material_0 = 1.0
    thickness_0 = T_0
    material_used_0 = W * thickness_0
    material_collected_0 = material_used_0 * (1 - l)
    property_of_collected_0 = property_of_raw_material_0 * (1 - p)

    denominator_1 = ((1 - R) * (1 - R**1 * (1 - p)**1)) / (1 - R * (1 - p)) + R**1 * (1 - p)**1
    thickness_1 = T_0 / denominator_1
    recycled_material_0 = thickness_1 * R * W
    downcycled_material_0 = material_collected_0 - recycled_material_0
    raw_X1_0 = property_of_collected_0 * downcycled_material_0
    raw_X2_0 = raw_X1_0 * (1 - l) * property_of_collected_0 * (1 - p)

    property_of_raw_material.append(property_of_raw_material_0)
    thickness.append(thickness_0)
    material_used.append(material_used_0)
    material_collected.append(material_collected_0)
    property_of_collected.append(property_of_collected_0)
    recycled_material.append(recycled_material_0)
    downcycled_material.append(downcycled_material_0)
    raw_material_saved_X1.append(raw_X1_0)
    raw_material_saved_X2.append(raw_X2_0)
    total_savings.append(0)
    cumulative_savings.append(0)

    for i in range(1, n + 1):
        denominator_i = ((1 - R) * (1 - R**i * (1 - p)**i)) / (1 - R * (1 - p)) + R**i * (1 - p)**i
        prop_raw_i = denominator_i
        thickness_i = T_0 / denominator_i
        mat_used_i = W * thickness_i
        mat_collected_i = mat_used_i * (1 - l)
        prop_collected_i = prop_raw_i * (1 - p)

        denominator_ip1 = ((1 - R) * (1 - R**(i + 1) * (1 - p)**(i + 1))) / (1 - R * (1 - p)) + R**(i + 1) * (1 - p)**(i + 1)
        thickness_ip1 = T_0 / denominator_ip1
        rec_mat_i = thickness_ip1 * R * W
        down_mat_i = mat_collected_i - rec_mat_i

        raw_X1_i = prop_collected_i * down_mat_i
        raw_X2_i = raw_X1_i * (1 - l) * prop_collected_i * (1 - p)

        total_i = raw_material_saved_X1[i - 1] + recycled_material[i - 1] + (raw_material_saved_X2[i - 2] if i > 1 else 0)
        cumulative_i = cumulative_savings[i - 1] + total_i

        property_of_raw_material.append(prop_raw_i)
        thickness.append(thickness_i)
        material_used.append(mat_used_i)
        material_collected.append(mat_collected_i)
        property_of_collected.append(prop_collected_i)
        recycled_material.append(rec_mat_i)
        downcycled_material.append(down_mat_i)
        raw_material_saved_X1.append(raw_X1_i)
        raw_material_saved_X2.append(raw_X2_i)
        total_savings.append(total_i)
        cumulative_savings.append(cumulative_i)

    df = pd.DataFrame({
        'Cycle': range(0, n + 1),
        'Property of Raw Material': property_of_raw_material,
        'Thickness': thickness,
        'Material Used (kg)': material_used,
        'Material Collected (kg)': material_collected,
        'Property of Collected': property_of_collected,
        'Recycled Material (kg)': recycled_material,
        'Downcycled Material (kg)': downcycled_material,
        'Raw Material Saved for X1 (kg)': raw_material_saved_X1,
        'Raw Material Saved for X2 (kg)': raw_material_saved_X2,
        'Total Savings (kg)': total_savings,
        'Cumulative Savings (kg)': cumulative_savings
    })

    return df

df = recycling_model(W, R, p, n, l, T_0, pc)
st.write("### Recycling Output Table")
st.dataframe(df)

# Plotting
fig, ax = plt.subplots(3, 1, figsize=(12, 10))

# Total Savings
ax[0].plot(df['Cycle'], df['Total Savings (kg)'], marker='o')
ax[0].set_title("Total Savings per Cycle")
ax[0].set_ylabel("Total Savings (kg)")
ax[0].grid()

# Cumulative Savings
ax[1].plot(df['Cycle'], df['Cumulative Savings (kg)'], marker='o', color='orange')
ax[1].set_title("Cumulative Savings over Cycles")
ax[1].set_ylabel("Cumulative Savings (kg)")
ax[1].grid()

# Materials
ax[2].plot(df['Cycle'], df['Material Used (kg)'], label='Material Used')
ax[2].plot(df['Cycle'], df['Material Collected (kg)'], label='Material Collected')
ax[2].plot(df['Cycle'], df['Recycled Material (kg)'], label='Recycled Material')
ax[2].plot(df['Cycle'], df['Downcycled Material (kg)'], label='Downcycled Material')
ax[2].set_title("Material Flow over Cycles")
ax[2].set_xlabel("Cycle")
ax[2].set_ylabel("Material (kg)")
ax[2].legend()
ax[2].grid()

st.pyplot(fig)


# In[ ]:




