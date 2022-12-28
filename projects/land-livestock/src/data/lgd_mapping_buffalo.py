from pathlib import Path

import pandas as pd
from fuzzywuzzy import process

dir_path = Path.cwd()
raw_data_path = Path.joinpath(dir_path, "data", "raw")
interim_data_path = Path.joinpath(dir_path, "data", "interim")
processed_data_path = Path.joinpath(dir_path, "data", "processed")
ext_data_path = Path.joinpath(dir_path, "data", "external")

lgd = pd.read_csv(Path.joinpath(ext_data_path, "lgd_district.csv"))
lgd.drop(
    ["St_Cs2011_code", "St_Cs2001_code", "Dt_Cs2011_code", "Dt_Cs2001_code"],
    axis=1,
    inplace=True,
)
lgd = lgd.rename(
    columns={
        "State Name(In English)": "state",
        "District Name(In English)": "district",
    }
)

lgd["state_dist"] = ""
for i in range(0, 734):
    lgd["state_dist"][i] = lgd["state"][i].rstrip() + lgd["district"][i]

buffalo = pd.read_csv(Path.joinpath(processed_data_path, "buffalo.csv"))

for i in range(0, 1364):
    if buffalo["district_name"][i].upper() == "SORAIDEU":
        buffalo["district_name"][i] = "CHARAIDEO"
    if buffalo["district_name"][i].upper() == "SIBSAGAR":
        buffalo["district_name"][i] = "SIVASAGAR"
    if buffalo["district_name"][i].upper() == "MEWAT":
        buffalo["district_name"][i] = "NUH"
    if buffalo["district_name"][i].upper() == "KARGIL":
        buffalo["state_name"][i] = "LADAKH"
    if buffalo["district_name"][i].upper() == "LEH LADAKH":
        buffalo["state_name"][i] = "LADAKH"
    if buffalo["district_name"][i].upper() == "DADRA AND NAGAR HAVELI":
        buffalo["state_name"][i] = "THE DADRA AND NAGAR HAVELI AND DAMAN AND DIU"
    if buffalo["district_name"][i].upper() == "GULBARGA":
        buffalo["district_name"][i] = "KALABURAGI"
    if buffalo["district_name"][i].upper() == "MYSORE":
        buffalo["district_name"][i] = "MYSURU"
    if buffalo["district_name"][i].upper() == "BANGALORE RURAL":
        buffalo["district_name"][i] = "BENGALURU RURAL"
    if buffalo["district_name"][i].upper() == "SORAIDEU":
        buffalo["district_name"][i] = "CHARAIDEO"
    if buffalo["district_name"][i].upper() == "BELGAUM":
        buffalo["district_name"][i] = "BELAGAVI"
    if buffalo["district_name"][i].upper() == "BELLARY":
        buffalo["district_name"][i] = "BALLARI"
    if buffalo["district_name"][i].upper() in "NAWANSHAHR (SBS NAGAR)":
        buffalo["district_name"][i] = "SHAHID BHAGAT SINGH NAGAR"
    if buffalo["district_name"][i].upper() == "MUKTSAR":
        buffalo["district_name"][i] = "SRI MUKTSAR SAHIB"
    if buffalo["district_name"][i].upper() == "ALLAHABAD":
        buffalo["district_name"][i] = "PRAYAGRAJ"
    if buffalo["district_name"][i].upper() == "SANT RAVIDAS NAGAR":
        buffalo["district_name"][i] = "BHADOHI"
    if buffalo["district_name"][i].upper() == "BARDHAMAN":
        buffalo["district_name"][i] = "PURBA BARDHAMAN"
    if (buffalo["district_name"][i].upper() == "BIJAPUR") and (
        buffalo["state_name"][i].upper() == "KARNATAKA"
    ):
        buffalo["district_name"][i] = "VIJAYAPURA"

buffalo["state_name"] = buffalo["state_name"].str.upper()
buffalo["district_name"] = buffalo["district_name"].str.upper()
buffalo["state_dist"] = buffalo["state_name"] + buffalo["district_name"]

b1 = pd.merge(
    buffalo,
    lgd,
    how="outer",
    left_on="state_dist",
    right_on="state_dist",
    validate="m:1",
    indicator=True,
    suffixes=["_DATA", "_LGD"],
)

not_lgd_mapped = b1[(b1["_merge"] == "left_only")][
    [
        "state_name",
        "district_name",
        "state_dist",
    ]
]

not_lgd_mapped = not_lgd_mapped.drop_duplicates(subset="state_dist")

result = [
    process.extractOne(i, lgd["state_dist"]) for i in not_lgd_mapped["state_dist"]
]
result = pd.DataFrame(result, columns=["match", "score", "id"])
result.drop("id", axis=1, inplace=True)

not_lgd_proxy_df = (
    pd.DataFrame(not_lgd_mapped["state_dist"], index=None)
    .reset_index()
    .drop("index", axis=1)
)

mapper_df = pd.concat(
    [not_lgd_proxy_df, result],
    axis=1,
    ignore_index=True,
    names=["original", "match", "score"],
)

mapper_df = mapper_df[mapper_df[2] >= 90]
mapper_dict = dict(zip(mapper_df[0], mapper_df[1]))
buffalo["state_dist"] = buffalo["state_dist"].replace(mapper_dict)

b1 = pd.merge(
    buffalo,
    lgd,
    how="outer",
    left_on="state_dist",
    right_on="state_dist",
    validate="m:1",
    indicator=True,
    suffixes=["_DATA", "_LGD"],
)

not_lgd_mapped = b1[(b1["_merge"] == "left_only")][
    [
        "state_name",
        "district_name",
        "state_dist",
    ]
]
not_lgd_mapped = not_lgd_mapped.drop_duplicates(subset="state_dist")

result = [
    process.extractOne(i, lgd["state_dist"]) for i in not_lgd_mapped["state_dist"]
]
result = pd.DataFrame(result, columns=["match", "score", "id"])
result.drop("id", axis=1, inplace=True)

not_lgd_proxy_df = (
    pd.DataFrame(not_lgd_mapped["state_dist"], index=None)
    .reset_index()
    .drop("index", axis=1)
)

mapper_df = pd.concat(
    [not_lgd_proxy_df, result],
    axis=1,
    ignore_index=True,
    names=["original", "match", "score"],
)

mapper_df = mapper_df[mapper_df[2] >= 90]
mapper_dict = dict(zip(mapper_df[0], mapper_df[1]))
buffalo["state_dist"] = buffalo["state_dist"].replace(mapper_dict)

b1 = pd.merge(
    buffalo,
    lgd,
    how="outer",
    left_on="state_dist",
    right_on="state_dist",
    validate="m:1",
    indicator=True,
    suffixes=["_DATA", "_LGD"],
)

not_lgd_mapped = b1[(b1["_merge"] == "left_only")][
    [
        "state_name",
        "district_name",
        "state_dist",
    ]
]
not_lgd_mapped = not_lgd_mapped.drop_duplicates(subset="state_dist")

not_lgd_mapped.to_csv("buffalo_unmapped.csv")

b2 = b1[b1["_merge"] == "both"]

b2 = b2.drop(["_merge", "state", "district"], axis=1)

cols = b2.columns.to_list()

cols = [
    "state_name",
    "district_name",
    "state_dist",
    "St_LGD_code",
    "Dt_LGD_code",
    "female",
    "upto_two_years",
    "used_for_breeding_only",
    "used_for_agri_only",
    "used_for_agri_and_breeding",
    "bullock_cart_farm_op",
    "others",
    "under_one_year",
    "one_to_three_years",
    "in_milk",
    "dry",
    "not_calved_once",
    "total_male",
    "total_female",
    "total",
]

b2 = b2[cols]

b2.to_csv(Path.joinpath(processed_data_path, "buffalo_lgd.csv"), index=False)

buffalo = pd.read_csv(Path.joinpath(processed_data_path, "buffalo_lgd.csv"))

buffalo.drop(["state_dist"], axis=1, inplace=True)
buffalo.rename(
    columns={
        "St_LGD_code": "state_lgd_code",
        "Dt_LGD_code": "district_lgd_code",
    },
    inplace=True,
)

buffalo.to_csv(Path.joinpath(processed_data_path, "buffalo_lgd.csv"), index=False)
