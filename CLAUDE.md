# Planets

Space, with real planets. Build a rocket, fly up, and land on the Moon, Mars,
Venus or Pluto.

This file is read automatically whenever Claude Code is opened in this folder.
Everything below is specific to this one mod. The general rules about how to
work with Elduin live in `~/.claude/CLAUDE.md`.

## Facts about this mod

    mod id            planets               (underscores — never change this)
    slug              planets-mod           (repo name and Modrinth slug)
    package           com.elduin.planets
    loader            fabric                (only fabric — see below)
    minecraft         1.21.1, 1.21.4
    primary version   1.21.1                (the one he plays)
    java              21 for both — Gradle picks this per version

The mod id is baked into save files. Once a world has been played with this mod,
**changing the mod id breaks that world.** Rename the display name freely;
never rename the mod id.

## How the mod is put together

    Planet.java              the list of worlds, their gravity and whether you can breathe
    block/RocketBlock        right-click opens the launch screen
    client/LaunchScreen      the planet picker (client only)
    net/LaunchPayload        client -> server "take me to planet N"
    space/SpaceTravel        teleporting, finding the ground, building the landing pad
    space/SpaceEffects       low gravity and suffocation, once a second on the server tick

Adding a planet means: a new `Planet` enum entry, a new entry in the `PLANETS`
list in the generator script (see below), and three new block textures.

## The datapack is written twice, on purpose

1.21.2 changed the shape of recipe ingredient keys (`{"item": "x"}` became just
`"x"`) and of a biome's `carvers` field (a map keyed by carving step became a
plain list). Stonecutter only rewrites Java, not json, so **everything under
`data/` lives per-version**:

    src/overrides/1.21.1/resources/data/...
    src/overrides/1.21.4/resources/data/...

`build.fabric.gradle.kts` adds the matching folder as a resource dir. Assets
(textures, models, lang) are shared in `src/main/resources` — `assets/planets/items/`
is the 1.21.4+ item model format and 1.21.1 simply ignores the folder.

**Folder names are not a difference.** 1.21 already singularised them, so both
versions want `recipe/`, `loot_table/`, `advancement/` and `tags/block/`. The
plural names were used here at first and the failure is completely silent — the
files simply never load, so recipes don't appear and blocks drop nothing. If
something in `data/` seems to be ignored, check the folder name against the
vanilla jar before anything else:

    unzip -l ~/.gradle/caches/fabric-loom/<ver>/minecraft-client.jar | grep data/minecraft/

Both trees are written by a generator script rather than by hand. If you change
one, change the generator, not the json.

## Layout

Multi-version is handled by [Stonecutter](https://plugins.gradle.org/plugin/dev.kikugie.stonecutter):
one source tree, version-conditional comments, many outputs.

    src/main/java/com/elduin/planets/        the mod
    src/main/resources/                      assets, mixins, lang
    src/overrides/<mcversion>/resources/     the data pack, once per version
    versions/<mcversion>-fabric/build/libs/  built jars land here
    stonecutter.properties.toml              mod id, name, version, dependencies
    settings.gradle.kts                      the Minecraft version list

There is **no `fabric.mod.json` file** — it is generated at build time from
`stonecutter.properties.toml` by the code in `build-logic/`. Same for
`mod.version`: there is no `mod_version` in `gradle.properties`.

Do **not** add a branch or a repo for a new Minecraft version. Add it to the
list in `settings.gradle.kts`, add a matching `[fabric."<version>"]` block in
`stonecutter.properties.toml`, add it to the matrix in
`.github/workflows/release.yml`, add a `src/overrides/<version>/` data tree, and
fix whatever stops compiling.

## Fabric only

He has asked for Forge and NeoForge. The answer is still no, and it is not a
preference: each extra loader is another full copy of Minecraft to decompile,
and this is an 8 GB machine. Two Minecraft versions on one loader is already
close to the ceiling. Do not add them back, and say so plainly if he asks again.

For the same reason `gradle.properties` sets `org.gradle.parallel=false`.

## Commands

    ./gradlew "Set active project to 1.21.1-fabric"   switch versions first
    ./gradlew "1.21.1-fabric:build"                   build just that version
    ./gradlew build                                   build every version
    ./gradlew runActiveClient                         launch a dev client

Switching rewrites the shared source tree into that version's form. It is **not**
required before building — each version subproject regenerates its own sources,
so the jars are correct either way.

Never hand-edit `.sc_active_version`. Use the task above and nothing else.

## Conventions for this repo

- Textures are 16x16. Block textures are generated procedurally, item icons are
  hand-drawn pixel maps — both in the generator script, so they stay consistent.
- Every new block and item needs an entry in `assets/planets/lang/en_us.json`,
  or it shows up in-game as a raw id, which reads to him as "broken".
- No dependencies beyond Fabric API.

## Releasing

Handled by the **share-it** skill. Bump `mod.version` in
`stonecutter.properties.toml`, update `CHANGELOG.md` in plain words, push a
`v<version>` tag, and the workflow builds both versions and publishes.
