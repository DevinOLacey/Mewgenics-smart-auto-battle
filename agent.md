# Smart AutoBattle - Current State

This document describes the live state of the mod in this folder.

## Mod Goal

- Give classes distinct smart AI presets.
- Keep the smart AI logic readable and tunable through per-class presets plus per-ability scoring.
- Apply smart AI to player cats through real class passive instances rather than broad class hooks.

## Current Live Hooks

### 1. Passive-instance routing is active

Files:
- `data/passives/fighter_passives.gon.patch`
- `data/passives/hunter_passives.gon.patch`
- `data/passives/medic_passives.gon.patch`
- `data/passives/mage_passives.gon.patch`
- `data/passives/tank_passives.gon.patch`
- `data/passives/thief_passives.gon.patch`
- `data/passives/butcher_passives.gon.patch`
- `data/passives/psychic_passives.gon.patch`
- `data/passives/colorless_passives.gon.patch`
- `data/passives/jester_passives.gon.patch`
- `data/passives/druid_passives.gon.patch`
- `data/passives/monk_passives.gon.patch`
- `data/passives/necromancer_passives.gon.patch`
- `data/passives/tinkerer_passives.gon.patch`

Current behavior:
- `Uncontrollable 1`
- `ReplaceBrain { brain GenericBrain decision_weights smart_* move_weights smart_*_move }`
- The AI carrier now lives on real passive records for each class.
- This is the current player-safe routing strategy.

### 2. PlayerCat is only a GenericBrain fallback

File:
- `data/characters/player_cat.gon.patch`

Current behavior:
```gon
PlayerCat.merge {
    ai {
        brain GenericBrain
    }
}
```

Important:
- This does not by itself force autobattle.
- The active autobattle carrier logic now comes from the passive-route patches.

## Disabled / Non-Active Experiments

These files are currently not part of the active strategy:
- `data/classes/classes.gon.patch`
- `data/classes/advanced_classes.gon.patch`

Those were part of the old broad class-routing path and are intentionally disabled/removed.

## AI Presets

Files:
- `data/ai_presets/decision_presets.gon.patch`
- `data/ai_presets/move_presets.gon.patch`

Notable current tuning:
- `smart_fighter.kill_enemy 15`
- `smart_thief.kill_enemy 15`
- `smart_butcher.kill_enemy 15`
- `smart_hunter.kill_enemy 20`
- `smart_mage.kill_enemy 15`
- `smart_cleric.revive_ally_corpse 250`

## AI Preset Field Reference (What values mean + allowed formats)

This section is a quick reference for tuning the fields used in `decision_presets` and `move_presets`.

### Move preset fields (`smart_*_move`)

- `distance_to_enemy`
  - Purpose: prefer being closer/farther from enemies.
  - Value type: number (int or decimal).
  - Typical interpretation: lower/negative = close in, higher/positive = keep distance.

- `distance_to_ally`
  - Purpose: control spacing relative to allies (group up or spread out).
  - Value type: number (int or decimal).
  - Typical interpretation: negative = cluster, positive = separate.

- `distance_to_character`
  - Purpose: generic spacing pressure against any character body.
  - Value type: number (int or decimal).

- `distance_to_corpse`
  - Purpose: attraction/avoidance to corpses (important for necro logic).
  - Value type: number (int or decimal).
  - Typical interpretation: negative = seek corpses, positive = avoid corpses.

- `preferred_distance`
  - Purpose: target spacing band in tiles.
  - Allowed formats:
    - Numeric distance: `0`, `1`, `3`, `8`, etc.
    - Dynamic keywords/expressions used by vanilla and this mod: `reach`, `mov`, `mov+reach`, `mov+N`, `mov-N`.

- `total_distance_moved`
  - Purpose: how much the AI values moving at all on its turn.
  - Value type: number (int or decimal, usually `0.0` to `1.5` in practice).
  - Practical note: `0` minimizes idle drift/burned bonus-move repositioning.

- `face_closest_enemy`
  - Purpose: orientation preference toward nearest enemy.
  - Value type: numeric weight (commonly `0` or `1`).

- `danger_avoidance`
  - Purpose: avoid dangerous tiles/paths.
  - Value type: number (int or decimal), usually non-negative.
  - Higher = safer movement preference.

- `tall_grass`
  - Purpose: preference for tall-grass tiles.
  - Value type: number (int or decimal), usually non-negative.

- `randomness`
  - Purpose: inject non-deterministic path choice.
  - Value type: number (int or decimal), usually non-negative.

### Decision preset fields (`smart_*`)

- Core action-category weights (all numeric int/decimal):
  - `damage_ally`, `damage_enemy`
  - `heal_ally`, `heal_enemy`
  - `kill_enemy`, `kill_ally`
  - `debuff_ally`, `debuff_enemy`
  - `buff_ally`, `buff_enemy`
  - `damage_self`, `heal_self`
  - `buff_self`, `debuff_self`
  - `damage_ally_corpse`, `damage_enemy_corpse`
  - `revive_ally_corpse`, `revive_enemy_corpse`
  - `spawn_object`
  - Typical interpretation: positive = incentivize, negative = penalize.

- Spawn placement helpers:
  - `spawn_object_distance_to_enemy`
  - `spawn_object_distance_to_ally`
  - `spawn_object_preferred_distance`
  - Value type: number (int or decimal).
  - Purpose: where deployables/traps/summons should be placed.

- Global scaling knobs:
  - `negative_weight_scale` (number, usually `0` to `1`; dampens negative outcomes)
  - `spend_mana_scale` (number, usually `0` to `1`; lower = spends mana more freely)

- Boolean toggles (allowed values: `true` / `false`):
  - `consider_total_damage`
  - `consider_secondary_damage`
  - `consider_aoe`
  - `accurate_knockback`
  - `consider_overkill`

### Practical value conventions used in this project

- Strong hard-deny in ability scoring: `-99999` or `-999999`.
- Soft discourage: around `-1` to `-8`.
- Neutral: `0`.
- Light encourage: `1` to `5`.
- High priority: `8+` (context-sensitive per class and ability).

## Current Charm-Kill Tuning

Execution-style attacks in the main damage classes now include a moderate `Charmed` target penalty.

Touched files:
- `data/abilities/fighter_abilities.gon.patch`
- `data/abilities/hunter_abilities.gon.patch`
- `data/abilities/mage_abilities.gon.patch`

Current intent:
- Prefer killing a non-charmed target when a similar kill is available.
- Still allow killing a charmed target if the alternative is only weak chip damage.

## Working Assumptions

At the time of this document, the intended live path is:
- Smart AI is applied through real passive instances.
- The disorder-based route is no longer part of the mod.
- The old broad class-routing hook should remain disabled.

## Editing Rules

- Keep GON patch files ASCII.
- Prefer `.merge` and patching over redefining vanilla objects.
- Re-check mod load behavior in-game after any hook change; several earlier tests were confounded by injection/load issues.
