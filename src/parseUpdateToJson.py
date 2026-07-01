from datetime import datetime

historic_key_list = [
  'time_span', 'agent_name', 'agent_faction', 'date_(yyyy-mm-dd)', 'time_(hh:mm:ss)', 'level',
  'lifetime_ap', 'current_ap', 'unique_portals_visited', 'unique_portals_drone_visited',
  'furthest_drone_distance', 'seer_points', 'xm_collected', 'opr_agreements',
  'portal_scans_uploaded', 'uniques_scout_controlled', 'resonators_deployed',
  'links_created', 'control_fields_created', 'mind_units_captured',
  'longest_link_ever_created', 'largest_control_field', 'xm_recharged',
  'portals_captured', 'unique_portals_captured', 'mods_deployed', 'hacks',
  'drone_hacks', 'glyph_hack_points', 'overclock_hack_points', 'completed_hackstreaks',
  'longest_sojourner_streak', 'resonators_destroyed', 'portals_neutralized',
  'enemy_links_destroyed', 'enemy_fields_destroyed', 'battle_beacon_combatant',
  'drones_returned', 'machina_links_destroyed', 'machina_resonators_destroyed',
  'machina_portals_neutralized', 'machina_portals_reclaimed', 'max_time_portal_held',
  'max_time_link_maintained', 'max_link_length_x_days', 'max_time_field_held',
  'largest_field_mus_x_days', 'forced_drone_recalls', 'distance_walked',
  'kinetic_capsules_completed', 'unique_missions_completed', 'research_bounties_completed',
  'research_days_completed', 'mission_day(s)_attended', 'nl-1331_meetup(s)_attended',
  'first_saturday_events', 'second_sunday_events', 'agents_recruited',
  'recursions', 'months_subscribed', 'orion_tokens', 'orion_link_and_field_points', 'apollo_tokens'
]

def parseUpdateToJson(raw_update):
    keys, values = raw_update.lower().strip().split('\n')
    values = values.replace("all time", "all_time", 1)

    keys_list = keys.strip().split(' ')
    values_list = values.strip().split(' ')

    json_update = {}
    value_counter = 0
    statname = ''
    for word in keys_list:
        if statname != '':
            statname += '_'
        statname += word
        if statname in historic_key_list:
            json_update[statname] = values_list[value_counter]
            value_counter += 1
            statname = ''
    # print(json_update)
    return json_update


def getIsoDtFromJsonUpdate(jsonUpdate): 
    date_str = jsonUpdate.get("date_(yyyy-mm-dd)")
    time_str = jsonUpdate.get("time_(hh:mm:ss)")

    if not date_str or not time_str:
        raise ValueError("Missing date or time field")

    # Combine and parse
    dt = datetime.strptime(
        f"{date_str} {time_str}",
        "%Y-%m-%d %H:%M:%S"
    )
    return dt


def firstDTIsBeforeEqualsSecondDT(update1, update2):
    dt1 = getIsoDtFromJsonUpdate(update1)
    dt2 = getIsoDtFromJsonUpdate(update2)
    return dt1 <= dt2
    
