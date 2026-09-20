#!/usr/bin/env python3
"""Writes every json file the Planets mod needs.

Assets are shared by both Minecraft versions. Data packs are not: 1.21.2
renamed a pile of datapack folders (loot_tables -> loot_table, recipes ->
recipe, tags/blocks -> tags/block) and changed the shape of recipe keys and of
a biome's "carvers" field. So everything under data/ is written twice, into
per-version override roots that build.fabric.gradle.kts adds as resource dirs.
"""
import json, os

REPO = "/Users/elduinnunn/GitHub/planets-mod"
ASSETS = os.path.join(REPO, "src/main/resources/assets/planets")
VERSIONS = ["1.21.1", "1.21.4"]


def w(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
        f.write("\n")


def data_root(version):
    return os.path.join(REPO, "src/overrides", version, "resources/data")


def old(version):
    """True for the pre-1.21.2 datapack layout."""
    return version == "1.21.1"


# --------------------------------------------------------------------------
# the planets themselves
# --------------------------------------------------------------------------
PLANETS = [
    dict(
        id="moon", name="The Moon",
        rock="moon_rock", soil="moon_dust", ore="moonstone_ore", gem="moonstone",
        rock_name="Moon Rock", soil_name="Moon Dust",
        ore_name="Moonstone Ore", gem_name="Moonstone",
        effects="minecraft:the_end", fixed_time=18000, ambient=0.55,
        sky=0x05060F, fog=0x0A0C18, temperature=0.2, precipitation=False,
        ultrawarm=False,
        ground_low=52, ground_high=86, hills=0.55, bumps=0.20,
        ore_count=10, ore_size=6, ore_min=-48, ore_max=72,
        blurb="Grey, dusty and full of craters. You jump enormously high here.",
    ),
    dict(
        id="mars", name="Mars",
        rock="mars_rock", soil="mars_sand", ore="mars_crystal_ore", gem="mars_crystal",
        rock_name="Mars Rock", soil_name="Mars Sand",
        ore_name="Mars Crystal Ore", gem_name="Mars Crystal",
        effects="minecraft:overworld", fixed_time=6000, ambient=0.25,
        sky=0xD98E5A, fog=0xB8683A, temperature=0.0, precipitation=False,
        ultrawarm=False,
        ground_low=56, ground_high=104, hills=0.85, bumps=0.30,
        ore_count=8, ore_size=5, ore_min=-52, ore_max=64,
        blurb="Red rock and giant canyons. The sky is orange all day long.",
    ),
    dict(
        id="venus", name="Venus",
        rock="venus_rock", soil="venus_ash", ore="sulfur_ore", gem="sulfur",
        rock_name="Venus Rock", soil_name="Venus Ash",
        ore_name="Sulfur Ore", gem_name="Sulfur",
        effects="minecraft:overworld", fixed_time=6000, ambient=0.35,
        sky=0xE0B33A, fog=0xC9922A, temperature=2.0, precipitation=False,
        ultrawarm=True,
        ground_low=54, ground_high=92, hills=0.70, bumps=0.35,
        ore_count=12, ore_size=7, ore_min=-52, ore_max=72,
        blurb="Yellow, hot and horrible. Water boils away the moment you pour it.",
    ),
    dict(
        id="pluto", name="Pluto",
        rock="pluto_ice", soil="pluto_snow", ore="frost_ore", gem="frost_shard",
        rock_name="Pluto Ice", soil_name="Pluto Snow",
        ore_name="Frost Ore", gem_name="Frost Shard",
        effects="minecraft:the_end", fixed_time=18000, ambient=0.35,
        sky=0x101A3C, fog=0x18224A, temperature=-0.7, precipitation=True,
        ultrawarm=False,
        ground_low=50, ground_high=78, hills=0.40, bumps=0.15,
        ore_count=9, ore_size=6, ore_min=-48, ore_max=68,
        blurb="Tiny, frozen and a very long way out. Almost no gravity at all.",
    ),
]

ROCK_BLOCKS = [p["rock"] for p in PLANETS]
SOIL_BLOCKS = [p["soil"] for p in PLANETS]
ORE_BLOCKS = [p["ore"] for p in PLANETS]
GEMS = [p["gem"] for p in PLANETS]
ALL_BLOCKS = ROCK_BLOCKS + SOIL_BLOCKS + ORE_BLOCKS + ["rocket"]


# --------------------------------------------------------------------------
# assets: blockstates, models, item model definitions
# --------------------------------------------------------------------------
def cube(name):
    w(os.path.join(ASSETS, "blockstates", name + ".json"),
      {"variants": {"": {"model": "planets:block/" + name}}})
    w(os.path.join(ASSETS, "models/block", name + ".json"),
      {"parent": "minecraft:block/cube_all", "textures": {"all": "planets:block/" + name}})
    w(os.path.join(ASSETS, "models/item", name + ".json"),
      {"parent": "planets:block/" + name})


def flat_item(name, texture=None):
    w(os.path.join(ASSETS, "models/item", name + ".json"),
      {"parent": "minecraft:item/generated",
       "textures": {"layer0": "planets:item/" + (texture or name)}})


def item_definition(name):
    """1.21.4+ reads assets/<ns>/items/<id>.json. 1.21.1 ignores the folder."""
    w(os.path.join(ASSETS, "items", name + ".json"),
      {"model": {"type": "minecraft:model", "model": "planets:item/" + name}})


def box(f, t, tex, shade=True):
    faces = {d: {"texture": tex} for d in ("north", "south", "east", "west", "up", "down")}
    e = {"from": f, "to": t, "faces": faces}
    if not shade:
        e["shade"] = False
    return e


def rocket_model():
    return {
        "parent": "minecraft:block/block",
        "ambientocclusion": False,
        "textures": {
            "particle": "planets:block/rocket",
            "side": "planets:block/rocket",
            "nose": "planets:block/rocket_nose",
        },
        "elements": [
            box([5, 0, 5], [11, 13, 11], "#side"),
            box([6, 13, 6], [10, 16, 10], "#nose"),
            box([7, 0, 3], [9, 5, 5], "#nose"),
            box([7, 0, 11], [9, 5, 13], "#nose"),
            box([3, 0, 7], [5, 5, 9], "#nose"),
            box([11, 0, 7], [13, 5, 9], "#nose"),
        ],
    }


def write_assets():
    for name in ROCK_BLOCKS + SOIL_BLOCKS + ORE_BLOCKS:
        cube(name)
        item_definition(name)

    w(os.path.join(ASSETS, "blockstates/rocket.json"),
      {"variants": {"": {"model": "planets:block/rocket"}}})
    w(os.path.join(ASSETS, "models/block/rocket.json"), rocket_model())
    flat_item("rocket", "rocket_part")
    item_definition("rocket")

    for gem in GEMS:
        flat_item(gem)
        item_definition(gem)
    flat_item("oxygen_tank")
    item_definition("oxygen_tank")

    lang = {"itemGroup.planets": "Planets"}
    for p in PLANETS:
        lang["block.planets." + p["rock"]] = p["rock_name"]
        lang["block.planets." + p["soil"]] = p["soil_name"]
        lang["block.planets." + p["ore"]] = p["ore_name"]
        lang["item.planets." + p["gem"]] = p["gem_name"]
        lang["planets.planet." + p["id"]] = p["name"]
        lang["planets.blurb." + p["id"]] = p["blurb"]
    lang.update({
        "block.planets.rocket": "Rocket",
        "item.planets.oxygen_tank": "Oxygen Tank",
        "planets.planet.overworld": "Earth",
        "planets.blurb.overworld": "Home. Grass, trees, air you can actually breathe.",
        "planets.screen.title": "Where do you want to go?",
        "planets.screen.here": "You are here",
        "planets.screen.gravity": "Gravity: %s",
        "planets.message.launch": "Blast off to %s!",
        "planets.message.arrived": "Welcome to %s",
        "planets.message.no_oxygen": "You can't breathe out here! You need an Oxygen Tank.",
        "planets.message.no_rocket": "You need to be standing next to a rocket.",
        "planets.tooltip.oxygen_tank": "Lets you breathe on other planets. Just carry it.",
        "planets.tooltip.rocket": "Place it down, then right-click to fly.",
        "death.attack.planets.vacuum": "%1$s ran out of air",
    })
    w(os.path.join(ASSETS, "lang/en_us.json"), lang)


# --------------------------------------------------------------------------
# data: worldgen
# --------------------------------------------------------------------------
def dimension_type(p):
    return {
        "ultrawarm": p["ultrawarm"],
        "natural": False,
        "piglin_safe": False,
        "respawn_anchor_works": False,
        "bed_works": False,
        "has_raids": False,
        "has_skylight": True,
        "has_ceiling": False,
        "coordinate_scale": 1.0,
        "ambient_light": p["ambient"],
        "fixed_time": p["fixed_time"],
        "logical_height": 384,
        "effects": p["effects"],
        "infiniburn": "#minecraft:infiniburn_overworld",
        "min_y": -64,
        "height": 384,
        "monster_spawn_light_level": 0,
        "monster_spawn_block_light_limit": 0,
    }


def dimension(p):
    return {
        "type": "planets:" + p["id"],
        "generator": {
            "type": "minecraft:noise",
            "settings": "planets:" + p["id"],
            "biome_source": {"type": "minecraft:fixed", "biome": "planets:" + p["id"]},
        },
    }


def noise_settings(p):
    terrain = {
        "type": "minecraft:add",
        "argument1": {
            "type": "minecraft:add",
            "argument1": {
                "type": "minecraft:y_clamped_gradient",
                "from_y": p["ground_low"], "to_y": p["ground_high"],
                "from_value": 1.2, "to_value": -1.2,
            },
            "argument2": {
                "type": "minecraft:mul",
                "argument1": p["hills"],
                "argument2": {
                    "type": "minecraft:noise",
                    "noise": "minecraft:continentalness",
                    "xz_scale": 0.35, "y_scale": 0.0,
                },
            },
        },
        "argument2": {
            "type": "minecraft:mul",
            "argument1": p["bumps"],
            "argument2": {
                "type": "minecraft:noise",
                "noise": "minecraft:erosion",
                "xz_scale": 1.1, "y_scale": 0.0,
            },
        },
    }
    return {
        "sea_level": -64,
        "disable_mob_generation": True,
        "aquifers_enabled": False,
        "ore_veins_enabled": False,
        "legacy_random_source": False,
        "default_block": {"Name": "planets:" + p["rock"]},
        "default_fluid": {"Name": "minecraft:air"},
        "noise": {"min_y": -64, "height": 384, "size_horizontal": 1, "size_vertical": 2},
        "spawn_target": [],
        "noise_router": {
            "barrier": 0,
            "fluid_level_floodedness": 0,
            "fluid_level_spread": 0,
            "lava": 0,
            "temperature": 0,
            "vegetation": 0,
            "continents": 0,
            "erosion": 0,
            "depth": 0,
            "ridges": 0,
            "initial_density_without_jaggedness": 0,
            "final_density": terrain,
            "vein_toggle": 0,
            "vein_ridged": 0,
            "vein_gap": 0,
        },
        "surface_rule": {
            "type": "minecraft:sequence",
            "sequence": [
                {
                    "type": "minecraft:condition",
                    "if_true": {
                        "type": "minecraft:vertical_gradient",
                        "random_name": "minecraft:bedrock_floor",
                        "true_at_and_below": {"above_bottom": 0},
                        "false_at_and_above": {"above_bottom": 5},
                    },
                    "then_run": {"type": "minecraft:block",
                                 "result_state": {"Name": "minecraft:bedrock"}},
                },
                {
                    "type": "minecraft:condition",
                    "if_true": {
                        "type": "minecraft:stone_depth",
                        "offset": 0,
                        "add_surface_depth": True,
                        "secondary_depth_range": 0,
                        "surface_type": "floor",
                    },
                    "then_run": {"type": "minecraft:block",
                                 "result_state": {"Name": "planets:" + p["soil"]}},
                },
            ],
        },
    }


def biome(p, version):
    b = {
        "has_precipitation": p["precipitation"],
        "temperature": p["temperature"],
        "downfall": 0.4 if p["precipitation"] else 0.0,
        "effects": {
            "sky_color": p["sky"],
            "fog_color": p["fog"],
            "water_color": 0x3F76E4,
            "water_fog_color": 0x050533,
        },
        "spawners": {k: [] for k in
                     ("monster", "creature", "ambient", "axolotls",
                      "underground_water_creature", "water_creature",
                      "water_ambient", "misc")},
        "spawn_costs": {},
        # 1.21.2 turned this from a map keyed by carving step into a plain list
        "carvers": {} if old(version) else [],
        "features": [[], [], [], [], [], [], ["planets:" + p["ore"]]],
    }
    return b


def configured_ore(p):
    return {
        "type": "minecraft:ore",
        "config": {
            "discard_chance_on_air_exposure": 0.0,
            "size": p["ore_size"],
            "targets": [{
                "target": {"predicate_type": "minecraft:block_match",
                           "block": "planets:" + p["rock"]},
                "state": {"Name": "planets:" + p["ore"]},
            }],
        },
    }


def placed_ore(p):
    return {
        "feature": "planets:" + p["ore"],
        "placement": [
            {"type": "minecraft:count", "count": p["ore_count"]},
            {"type": "minecraft:in_square"},
            {"type": "minecraft:height_range",
             "height": {"type": "minecraft:uniform",
                        "min_inclusive": {"absolute": p["ore_min"]},
                        "max_inclusive": {"absolute": p["ore_max"]}}},
            {"type": "minecraft:biome"},
        ],
    }


# --------------------------------------------------------------------------
# data: loot, tags, recipes
# --------------------------------------------------------------------------
def self_drop(block):
    return {
        "type": "minecraft:block",
        "pools": [{
            "rolls": 1,
            "bonus_rolls": 0,
            "entries": [{"type": "minecraft:item", "name": "planets:" + block}],
            "conditions": [{"condition": "minecraft:survives_explosion"}],
        }],
    }


def gem_drop(ore, gem):
    return {
        "type": "minecraft:block",
        "pools": [{
            "rolls": 1,
            "bonus_rolls": 0,
            "entries": [{"type": "minecraft:item", "name": "planets:" + gem}],
            "conditions": [{"condition": "minecraft:survives_explosion"}],
        }],
    }


def ingredient(version, item):
    return item if not old(version) else {"item": item}


def rocket_recipe(version):
    return {
        "type": "minecraft:crafting_shaped",
        "category": "misc",
        "pattern": [" I ", "IRI", "IFI"],
        "key": {
            "I": ingredient(version, "minecraft:iron_ingot"),
            "R": ingredient(version, "minecraft:redstone_block"),
            "F": ingredient(version, "minecraft:furnace"),
        },
        "result": {"id": "planets:rocket", "count": 1},
    }


def tank_recipe(version):
    return {
        "type": "minecraft:crafting_shaped",
        "category": "misc",
        "pattern": [" G ", "IGI", "III"],
        "key": {
            "G": ingredient(version, "minecraft:glass"),
            "I": ingredient(version, "minecraft:iron_ingot"),
        },
        "result": {"id": "planets:oxygen_tank", "count": 1},
    }


def write_data(version):
    root = data_root(version)
    ns = os.path.join(root, "planets")
    loot_dir = "loot_tables" if old(version) else "loot_table"
    recipe_dir = "recipes" if old(version) else "recipe"
    block_tag_dir = "blocks" if old(version) else "block"

    for p in PLANETS:
        w(os.path.join(ns, "dimension_type", p["id"] + ".json"), dimension_type(p))
        w(os.path.join(ns, "dimension", p["id"] + ".json"), dimension(p))
        w(os.path.join(ns, "worldgen/noise_settings", p["id"] + ".json"), noise_settings(p))
        w(os.path.join(ns, "worldgen/biome", p["id"] + ".json"), biome(p, version))
        w(os.path.join(ns, "worldgen/configured_feature", p["ore"] + ".json"), configured_ore(p))
        w(os.path.join(ns, "worldgen/placed_feature", p["ore"] + ".json"), placed_ore(p))
        for block in (p["rock"], p["soil"]):
            w(os.path.join(ns, loot_dir, "blocks", block + ".json"), self_drop(block))
        w(os.path.join(ns, loot_dir, "blocks", p["ore"] + ".json"), gem_drop(p["ore"], p["gem"]))
    w(os.path.join(ns, loot_dir, "blocks", "rocket.json"), self_drop("rocket"))

    # Running out of air needs its own damage type so the death message reads right.
    w(os.path.join(ns, "damage_type", "vacuum.json"),
      {"message_id": "planets.vacuum", "exhaustion": 0.0, "scaling": "never"})

    w(os.path.join(ns, recipe_dir, "rocket.json"), rocket_recipe(version))
    w(os.path.join(ns, recipe_dir, "oxygen_tank.json"), tank_recipe(version))

    mc = os.path.join(root, "minecraft/tags", block_tag_dir)
    w(os.path.join(mc, "mineable/pickaxe.json"),
      {"replace": False, "values": ["planets:" + b for b in ROCK_BLOCKS + ORE_BLOCKS + ["rocket"]]})
    w(os.path.join(mc, "mineable/shovel.json"),
      {"replace": False, "values": ["planets:" + b for b in SOIL_BLOCKS]})
    w(os.path.join(mc, "needs_stone_tool.json"),
      {"replace": False, "values": ["planets:" + b for b in ORE_BLOCKS]})


def main():
    write_assets()
    for v in VERSIONS:
        write_data(v)
    print("json written for", ", ".join(VERSIONS))


main()
