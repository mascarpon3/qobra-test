const getFullUsersData = (users, deals) => {
    var users = users.map(u => ({...u, ...{total_amount: 0, nb_deals: 0}}))
    for (var deal_index in deals){
        var deal = deals[deal_index]
        var user = users.find(u => u.id === deal.user)

        user.total_amount += deal.amount
        user.nb_deals += 1
    }
    return users
}

const computeCommissions = user => {
    const {partition_0, partition_1, partition_2} = splitTotalAmountByObjective(
        user.total_amount, user.objective
    ) 
    return {
        user_id : user.id,
        commission: 0.05 * partition_0 + 0.1 * partition_1 + 0.15 * partition_2,
    }
}


const splitTotalAmountByObjective = (total_amount, objective) => {
     // this function splits the amount according to which commission ratio is applied to it.
     return {
        partition_0: getPartition(total_amount, 0, 0.5 * objective),
        partition_1: getPartition(total_amount, 0.5 * objective, objective),
        partition_2: getPartition(total_amount, objective, Infinity)
    }
}


const getPartition = (value, bornInf, bornSup) => {
    if (value < bornInf){
        return 0
    } else if (value > bornSup) {
        return bornSup - bornInf
    } else {
        return value - bornInf
    }
}

const fs = require("fs")
var input = JSON.parse(fs.readFileSync("data/input.json"))

const users = getFullUsersData(input["users"], input["deals"])
const output = users.map(computeCommissions)

fs.writeFileSync("data/output.json", JSON.stringify(output), encoding="utf-8")
