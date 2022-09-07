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

const computeComissions = user => {
    const {partion_0, partion_1, partion_2} = splitTotalAmountByObjective(
        user.total_amount, user.objective
    ) 
    return {
        user_id : user.id,
        commision: 0.05 * partion_0 + 0.1 * partion_1 + 0.15 * partion_2,
    }
}


const splitTotalAmountByObjective = (total_amount, objective) => {
    return {
        partion_0: getPartition(total_amount, 0, 0.5 * objective),
        partion_1: getPartition(total_amount, 0.5 * objective, objective),
        partion_2: getPartition(total_amount, objective, Infinity)
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

var fs = require("fs")
var input = JSON.parse(fs.readFileSync("data/input.json"))
const users = getFullUsersData(input["users"], input["deals"])
const output = users.map(computeComissions)

console.log(output)
