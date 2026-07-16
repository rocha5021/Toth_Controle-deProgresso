from repositories import collectibles_repo


def list_titles(character_id):
    return sorted(collectibles_repo.unlocked_for_character("titles", character_id))


def list_achievements(character_id):
    return sorted(collectibles_repo.unlocked_for_character("achievements", character_id))


def list_imbuements(character_id):
    return sorted(collectibles_repo.unlocked_for_character("imbuements", character_id))
