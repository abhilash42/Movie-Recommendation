
from recommendation_data import dataset

print("Lisa rose LIW:{}\n".format(dataset['Lisa Rose']['Lady in the Water']))
print(dataset['Jack Matthews'])


from math import sqrt


def simi_score(person1,person2):
    both_viewed={}
    for item in dataset[person1]:
        if item in dataset[person2]:
            both_viewed[item]=1
        # Conditions to check they both have an common rating items
        if(len(both_viewed)==0):
            return 0
        
        #finding euclindean distance
        sum_of_euc_distance = []
        
        for item in dataset[person1]:
            if item in dataset[person2]:
                sum_of_euc_distance.append(pow(dataset[person1][item]-dataset[person2][item],2))
        
        sum_of_euc_distance = sum(sum_of_euc_distance)
        
        return 1/(1+sqrt(sum_of_euc_distance))
    
#finding people who are not at all similar to lisa rose
for item in dataset:
    if(simi_score('Lisa Rose',item)==0):
        print(item)
    
#simi_score('Lisa Rose','Jack Matthews')


#pearson correlation approach 
def pearson_correlation(person1,person2):
 
    # To get both rated items
    both_rated = {}
    for item in dataset[person1]:
        if item in dataset[person2]:
            both_rated[item] = 1
 
    number_of_ratings = len(both_rated)
    
    # Check no of ratings in common
    if number_of_ratings == 0:
        return 0
    
    person1_pref_sum = sum(dataset[person1][item] for item in both_rated)
    person2_pref_sum = sum(dataset[person2][item] for item in both_rated)
    
    person1_square_preferences_sum = sum(pow(dataset[person1][item],2)for item in both_rated)
    person2_square_preferences_sum = sum(pow(dataset[person2][item],2)for item in both_rated)
    
    prod_sum_of_both_users = sum(dataset[person1][item]*dataset[person2][item]for item in both_rated)
    
    numerator_value = prod_sum_of_both_users - (person1_pref_sum*person2_pref_sum/number_of_ratings)
    denominator_value = sqrt((person1_square_preferences_sum - pow(person1_pref_sum,2)/number_of_ratings) * (person2_square_preferences_sum -pow(person2_pref_sum,2)/number_of_ratings))

    if(denominator_value==0):
        return 0
    else:
        r = numerator_value/denominator_value
        return r
    
    
#print(pearson_correlation('Lisa Rose','Gene Seymour'))


def most_similar_persons(person,num_of_users):
    
    scores = [(pearson_correlation(person,other),other)for other in dataset if other!=person]
    
    scores.sort()
    scores.reverse()
    return scores[0:num_of_users]

print(most_similar_persons('Lisa Rose',3))  


def user_recommendations(person):
    totals={}
    sim_sums={}
    rankings_list=[]
    for other in dataset:
        if other==person:
            continue
        sim = pearson_correlation(person,other)
        
        if sim <=0:
            continue;
        for item in dataset[other]:
            if( item not in dataset[person] or dataset[person][item]==0 ):
                
                totals.setdefault(item,0)
                totals[item]+=dataset[other][item]*sim
                
                sim_sums.setdefault(item,0)
                sim_sums[item]+=sim
#     for item in totals:
#         print(totals[item])
    rankings = [(totals/sim_sums[item],item) for item,totals in totals.items()]
    rankings.sort()
    rankings.reverse()
    #print(rankings)
    recommendations_list = [recommend_item for score,recommend_item in rankings]
    return recommendations_list
print("Recommendations for Toby")
print(user_recommendations("Toby"))

