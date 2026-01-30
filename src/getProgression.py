import heapq
import math
from badges import badges

badge_tier = ["Bronze", "Silver", "Gold", "Platinum", "Onyx"]

def getBadgeLevel(curr, tier_amount):
    curr = int(curr)
    # case still locked
    if curr < tier_amount[0]:
        progress = round(curr/tier_amount[0], 4)
        return "Locked", progress 

    # case onyx
    if curr > tier_amount[-1]:
        progress = curr // tier_amount[-1]
        return badge_tier[-1], progress

    for i in range(len(tier_amount)):
        # case unlocked and not onyx
        if curr < tier_amount[i]:
            tier = badge_tier[i-1]
            progress = round(curr/tier_amount[i], 4)
            return tier, progress

# ============================================================================================================================

def getProgression(json_update):
    nonOnyxSort = []
    onyxSort = []
    badgeProgressionList = "<b>Badge Progression</b>\n\n"
    for key in json_update.keys():
        if key in badges:
            tier, progress = getBadgeLevel(json_update[key], badges[key]['tier_amount'])
            # print(key+": "+str(tier)+" "+str(progress))
            if tier != "Onyx":
                heapq.heappush(nonOnyxSort, (-progress, tier, key))
            elif tier == "Onyx":
                heapq.heappush(onyxSort, (-progress, tier, key))

    for i in range(len(nonOnyxSort)):
        progress, badge, key = heapq.heappop(nonOnyxSort)
        progress = -progress
        badgeProgressionList += f"{(progress*100):.2f}% | " + badge + " | " + badges[key]["name"] + " (" + key.replace("_", " ") + ")\n"
    
    badgeProgressionList += "\n"
    
    for i in range(len(onyxSort)):
        progress, badge, key = heapq.heappop(onyxSort)
        progress = -progress
        if int(json_update['recursions']) >= 1 and progress >= 2:
            badgeProgressionList += f"Recursed: {(progress)}x " + badge + " | " + badges[key]["name"] + " (" + key.replace("_", " ") + ")\n"
        else: 
            badgeProgressionList += f"{(progress)}x " + badge + " | " + badges[key]["name"] + " (" + key.replace("_", " ") + ")\n"
        

    return badgeProgressionList
