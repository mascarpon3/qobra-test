import pandas as pd
import json


def get_deal_id_to_current_amount(deals):
    # the data should be sorted but sorting it here is more secure
    return deals.sort_values("close_date").set_index("id").groupby("user")["amount"].cumsum().to_dict()


def compute_commission(deal):
    partition_0, partition_1, partition_2 = split_amount_by_objective(
        deal["amount"], deal["objective"], deal["previous_amount"]
    )
    return partition_0 * 0.05 + partition_1 * 0.1 + partition_2 * 0.15


def split_amount_by_objective(amount, objective, previous_amount):
    # this function splits the amount according to which commission ratio is applied to it.
    partition = (
        get_partition_value(amount, 0, max(0.5 * objective - previous_amount, 0)),
        get_partition_value(amount, max(0.5 * objective - previous_amount, 0), max(objective - previous_amount, 0)),
        get_partition_value(amount, max(objective - previous_amount, 0), float('inf'))
    )
    assert sum(partition) == amount
    return partition


def get_partition_value(value, born_inf, born_sup):
    if value < born_inf:
        return 0.0
    elif value > born_sup:
        return born_sup - born_inf
    else:
        return value - born_inf


if __name__ == "__main__":
    with open("data/input.json", "r") as f:
        input = json.load(f)

    users = pd.DataFrame(input["users"])

    deals = (
        pd.DataFrame(input["deals"])
        .assign(
            objective=lambda df: df['user'].map(users.set_index("id")["objective"]),
            current_amount=lambda df: df["id"].map(get_deal_id_to_current_amount(df)),
            previous_amount=lambda df: df["current_amount"] - df["amount"],
            commission=lambda df: df.apply(compute_commission, axis=1),
        )
    )

    output = [
        {
            "user_id": user_id,
            "commission": user.set_index("close_date")["commission"].to_dict()
        }
        for user_id, user in deals.groupby("user")
    ]

    with open("data/output.json", "w") as f:
        json.dump(output, f)
