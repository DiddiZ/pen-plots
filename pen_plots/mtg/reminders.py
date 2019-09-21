import re

_reminder_patterns = [
    # Deathtouch
    r' \(Any amount of damage (this deals|they deal) to a creature is enough to destroy it\.\)',
    # Defender
    # Double Strike
    # Enchant
    # Equip
    # First Strike
    # Flash
    r' \(You may cast this spell any time you could cast an instant\.\)',
    # Flying
    # Haste
    r' \((This creature|It) can attack and \{T\} (this turn|as soon as it comes under your control)\.\)',
    # Hexproof
    # Indestructible
    # Intimidate
    # Landwalk
    # Lifelink
    # Protection
    # Reach
    # Shroud
    # Trample
    r' \((This creature|It) can deal excess( combat)? damage to the player or planeswalker it\'s attacking\.\)',
    # Vigilance
    # Banding
    # Rampage
    # Cumulative Upkeep
    # Flanking
    # Phasing
    # Buyback
    # Shadow
    # Cycling
    # Echo
    # Horsemanship
    # Fading
    # Kicker
    r' \(You may pay an additional (\{[0-9BRGUW]+\})+ as you cast this spell\.\)',
    # Flashback
    r' \(You may cast this card from your graveyard for its flashback cost. Then exile it\.\)',
    # Madness
    # Fear
    # Morph
    # Amplify
    # Provoke
    # Storm
    # Affinity
    # Entwine
    # Modular
    # Sunburst
    # Bushido
    # Soulshift
    # Splice
    # Offering
    # Ninjutsu
    # Epic
    # Convoke
    r' \(Your creatures can help cast this spell\. Each creature you tap while casting this spell pays for \{1\} or one mana of that creature\'s color\.\)',
    # Dredge
    # Transmute
    # Bloodthirst
    # Haunt
    # Replicate
    # Forecast
    # Graft
    # Recover
    # Ripple
    # Split Second
    # Suspend
    # Vanishing
    # Absorb
    # Aura Swap
    # Delve
    # Fortify
    # Frenzy
    # Gravestorm
    # Poisonous
    # Transfigure
    # Champion
    # Changeling
    # Evoke
    # Hideaway
    # Prowl
    # Reinforce
    # Conspire
    # Persist
    # Wither
    # Retrace
    # Devour
    # Exalted
    # Unearth
    # Cascade
    # Annihilator
    # Level Up
    # Rebound
    # Totem Armor
    # Infect
    # Battle Cry
    # Living Weapon
    # Undying
    # Miracle
    # Soulbond
    # Overload
    # Scavenge
    # Unleash
    # Cipher
    # Evolve
    # Extort
    # Fuse
    # Bestow
    # Tribute
    # Dethrone
    # Hidden Agenda
    # Outlast
    # Prowess
    # Dash
    # Exploit
    # Menace
    # Renown
    # Awaken
    # Devoid
    # Ingest
    # Myriad
    # Surge
    # Skulk
    # Emerge
    # Escalate
    # Melee
    # Crew
    # Fabricate
    # Partner
    # Undaunted
    # Improvise
    # Aftermath
    # Embalm
    # Eternalize
    # Afflict
    # Ascend
    # Assist
    # Jump-Start
    # Mentor
    r' \(Whenever this creature attacks, put a \+1/\+1 counter on target attacking creature with lesser power\.\)',
    # Afterlife
    r' \(When this creature dies, create (a|two|three) 1/1 white and black Spirit creature tokens with flying\.\)',
    # Riot
    r' \((This creature enters|They enter) the battlefield with your choice of a \+1/\+1 counter or haste\.\)',
    # Spectacle

    # Scry
    r' \(To scry [0-9]+, look at the top card of your library, then you may put that card on the bottom of your library\.\)',
    # Adapt
    r' \(If this creature has no \+1/\+1 counters on it, put (a|two|three|four) \+1/\+1 counters? on it\.\)',
]


def _is_keyword_line(words):
    for i in range(len(words) - 1):
        if words[i][-1] != ',' and words[i] != 'First':
            return False
    return True


def strip_reminders(oracle_text):
    """
    Removes reminder texts for common keywords to shorten oracle texts.
    """
    # Remove reminder texts
    for reminder in _reminder_patterns:
        oracle_text = re.sub(reminder, '', oracle_text)

    return oracle_text


def join_keyword_lines(oracle_text):
    """
    Joins multiple lines consisting of keywords to a single line in order to shorten oracle texts.
    """
    # Join keywords on one line
    oracle_text_split = [line.split(' ') for line in oracle_text.split('\n')]
    if _is_keyword_line(oracle_text_split[0]):  # Oracle text starts with keyword line
        # Check if following line is keyword line, too
        while len(oracle_text_split) > 1 and _is_keyword_line(oracle_text_split[1]):
            # Join both lines comma separated
            oracle_text_split[0][-1] = oracle_text_split[0][-1] + ','
            oracle_text_split[0].extend(oracle_text_split[1])
            del oracle_text_split[1]
        oracle_text = '\n'.join([" ".join(s) for s in oracle_text_split])

    return oracle_text
