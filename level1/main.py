import pandas as pd
import json


def get_user_id_to_total_amount(deals):
    return deals.groupby("user")["amount"].sum().to_dict()


def get_user_id_to_nb_deals(deals):
    return deals.groupby("user")["amount"].count().to_dict()


def compute_commission(row):
    return row['total_amount'] * get_commission_ratio(row["nb_deals"]) + get_bonus(row["total_amount"])


def get_commission_ratio(nb_deals):
    if nb_deals in [1, 2]:
        return 0.1
    if nb_deals > 2:
        return 0.2
    else:
        raise f"nb_deal must be a positive integer, found {nb_deals} of type {type(nb_deals)}"


def get_bonus(total_amount):
    if total_amount >= 2000:
        return 500
    else:
        return 0


if __name__ == "__main__":
    with open("data/input.json", "r") as f:
        input = json.load(f)

    deals = pd.DataFrame(input["deals"])

    users = (
        pd.DataFrame(input["users"])
        .rename(columns={"id": "user_id"})
        .assign(
            total_amount=lambda df: df["user_id"].map(get_user_id_to_total_amount(deals)),
            nb_deals=lambda df: df["user_id"].map(get_user_id_to_nb_deals(deals)),
            commission=lambda df: df.apply(compute_commission, axis=1)
        )
    )

    output = {
        "commissions": list(users[["user_id", "commission"]].transpose().to_dict().values())
    }

    with open("data/output.json", "w") as f:
        json.dump(output, f)
