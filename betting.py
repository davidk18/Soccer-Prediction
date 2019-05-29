import csv
import datetime as dt
def test_betting_stategy(predictions, test_features, test_labels, test_results_info, edge, strategy):
    result = {
        'spend': 0,
        'return': 0,
    }
    stake = 10
    present = dt.datetime.now()
    future_selections = [[]for i in range(7)]
    selections = [[]for i in range(8)]

    for i in range(0, len(predictions)):
        probabilities = predictions[i]['probabilities']
        bookies_home_odds = test_features['odds-home'][i]
        bookies_away_odds = test_features['odds-away'][i]
        home_difference = probabilities[0] - (1 / bookies_home_odds)
        away_difference = probabilities[2] - (1 / bookies_away_odds)


        if home_difference > away_difference:
            if probabilities[0] > ((1 / bookies_home_odds) + edge):
                staking_strategy_multiplier = optimizeStakeForStrategy(test_features['odds-home'][i], strategy)
                optimised_stake = stake * staking_strategy_multiplier
                if present > test_results_info[2][i]: # + dt.timedelta(days=14)
                    selections[0].append(test_results_info[0][i])
                    selections[1].append(test_results_info[1][i])
                    selections[2].append(test_results_info[2][i])
                    selections[3].append(bookies_home_odds)
                    selections[5].append(optimised_stake)
                    selections[7].append(home_difference)
                    result['spend'] = result['spend'] + optimised_stake
                    if test_labels[i] == 'H':
                        bet_return = bookies_home_odds * optimised_stake
                        result['return'] = result['return'] + bet_return
                        selections[4].append("H - Won")
                        selections[6].append(bet_return)
                    else:
                        selections[4].append("H - Lost")
                        selections[6].append(0.0)

                else:
                    future_selections[0].append(test_results_info[0][i])
                    future_selections[1].append(test_results_info[1][i])
                    future_selections[2].append(test_results_info[2][i])
                    future_selections[3].append(bookies_home_odds)
                    future_selections[4].append("H")
                    future_selections[5].append(optimised_stake)
                    future_selections[6].append(round(home_difference, 2))
        else:
            if probabilities[2] > ((1 / bookies_away_odds) + edge):
                staking_strategy_multiplier = optimizeStakeForStrategy(bookies_away_odds, strategy)
                optimised_stake = stake * staking_strategy_multiplier
                if present > test_results_info[2][i]:
                    selections[0].append(test_results_info[0][i])
                    selections[1].append(test_results_info[1][i])
                    selections[2].append(test_results_info[2][i])
                    selections[3].append(bookies_away_odds)
                    selections[5].append(optimised_stake)
                    selections[7].append(away_difference)

                    result['spend'] = result['spend'] + optimised_stake
                    if test_labels[i] == 'A':
                        bet_return = bookies_away_odds * optimised_stake
                        result['return'] = result['return'] + bet_return
                        selections[4].append("A - Won")
                        selections[6].append(bet_return)
                    else:
                        selections[4].append("A - Lost")
                        selections[6].append(0.0)

                else:
                    future_selections[0].append(test_results_info[0][i])
                    future_selections[1].append(test_results_info[1][i])
                    future_selections[2].append(test_results_info[2][i])
                    future_selections[3].append(bookies_away_odds)
                    future_selections[4].append("A")
                    future_selections[5].append(optimised_stake)
                    future_selections[6].append(round(away_difference, 2))

    if result['spend'] > 0:
        result['performance'] = result['return'] / result['spend']
    else:
        result['performance'] = 0

    with open('Betting.csv', 'w', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(["Home", "Away", "Date", "Odds", "Bet", "S", "R", "Edge"])
        for i in range(0, len(selections[0])):
            writer.writerow([selections[0][i], selections[1][i], selections[2][i].strftime('%d-%m-%Y'),
                             selections[3][i], selections[4][i], selections[5][i], round(selections[6][i], 2), round(selections[7][i], 2)])

    with open('FuturePredictions.csv', 'w', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(["Home", "Away", "Date", "Odds", "P", "Stake", "Edge"])
        for i in range(0, len(future_selections[0])):
            writer.writerow([future_selections[0][i], future_selections[1][i], future_selections[2][i].strftime('%d-%m-%Y'),
                             future_selections[3][i], future_selections[4][i], future_selections[5][i], round(future_selections[6][i], 2)])
    return result


def optimizeStakeForStrategy(odds, strategy):
    low_stake_multipliers = [2.0, 1.5, 1.0, 0.75, 0.5, .25]
    low_stake_odds = [2.0, 3.0, 4.0, 8.0, 12.0, 100.0]

    med_stake_multipliers = [1.0, 2.0, 1.5, 0.8, 0.5]
    med_stake_odds = [2.0, 5.0, 8.0, 12.0, 100.0]

    high_stake_mulitpliers = [0.0, 1.0, 1.25, 1.5, 2.0]
    high_stake_odds = [3.0, 6.0, 9.0, 12.0, 100.0]

    if strategy == 'Low':
        for i in range(0, len(low_stake_multipliers)):
            if odds <= low_stake_odds[i]:
                return low_stake_multipliers[i]

    if strategy == 'Medium':
        for i in range(0, len(med_stake_multipliers)):
            if odds <= med_stake_odds[i]:
                return med_stake_multipliers[i]

    if strategy == 'High':
        for i in range(0, len(high_stake_mulitpliers)):
            if odds <= high_stake_odds[i]:
                return high_stake_mulitpliers[i]

    return 1.0
