import os
from itertools import product
energies = ["LE"]
treatment = ["N_F"]
method = ['both']
params = [(30, 80, 8.8), # 30-80 MHz range
        (30, 100, 10.1), # 30-100 MHz range
        (30, 125, 11.4), # 30-125 MHz range
        (30, 150, 12.5), # 30-150 MHz range
        (30, 200, 14.3), # 30-200 MHz range
        (50, 200, 13)] # 50-200 MZ range
for energy, treat, meth in product(energies, treatment, method):
    if energy == "LE":
        path_to_library = "/sps/grand/vdecoene/HERON/NuSimLibrary/TauLibrary_972Events_Eshower_2e7-1e9GeV_XYZCoordinates_CorrXmax.npz"
    else:
        path_to_library = "/sps/grand/vdecoene/HERON/NuSimLibrary/TauLibrary_250Events_Eshower_1e8-1e10GeV_XYZCoordinates_CorrXmax.npz"
    f_min, f_max = 50, 200 if "F" in treat else (0, 5000)
    noise_std = 13 if "N" in treat else 0
    for polar in ['X,Y', 'X,Z', 'Y,Z', 'X,Y,Z']:
        save_path = f"/sps/grand/pminodier/HERON_results/ADF_Fixed_'norm'{'_'+treat if treat != 'none' else ''}_{meth}_{f_min}_{f_max}_{polar}_v2"
        os.system(
            f"""sbatch scripts/cheat_recons_polar.sh \
                '--path_to_library {path_to_library} \
                --save_path {save_path} \
                --f_min {f_min} \
                --f_max {f_max} \
                --noise_std {noise_std} \
                --intens_method amplitude \
                --norm_weights True \
                --prior {True if meth in ["prior", "both"] else False} \
                --constant {True if meth in ["prior", "both"] else True} \
                --polars {polar}'""")
    
