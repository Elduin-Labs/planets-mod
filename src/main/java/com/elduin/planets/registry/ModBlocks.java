package com.elduin.planets.registry;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;

import com.elduin.planets.PlanetsMod;
import com.elduin.planets.block.RocketBlock;

import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;

public final class ModBlocks {

	/** Registration order, which is also the order they appear in the creative tab. */
	public static final List<Block> ALL = new ArrayList<>();

	public static Block MOON_ROCK;
	public static Block MOON_DUST;
	public static Block MOONSTONE_ORE;

	public static Block MARS_ROCK;
	public static Block MARS_SAND;
	public static Block MARS_CRYSTAL_ORE;

	public static Block VENUS_ROCK;
	public static Block VENUS_ASH;
	public static Block SULFUR_ORE;

	public static Block PLUTO_ICE;
	public static Block PLUTO_SNOW;
	public static Block FROST_ORE;

	public static Block ROCKET;

	private ModBlocks() {
	}

	public static void register() {
		MOON_ROCK = rock("moon_rock", MapColor.COLOR_LIGHT_GRAY, 1.6F);
		MOON_DUST = loose("moon_dust", MapColor.TERRACOTTA_WHITE);
		MOONSTONE_ORE = ore("moonstone_ore", MapColor.COLOR_LIGHT_GRAY);

		MARS_ROCK = rock("mars_rock", MapColor.COLOR_RED, 1.8F);
		MARS_SAND = loose("mars_sand", MapColor.TERRACOTTA_RED);
		MARS_CRYSTAL_ORE = ore("mars_crystal_ore", MapColor.COLOR_RED);

		VENUS_ROCK = rock("venus_rock", MapColor.COLOR_BROWN, 2.2F);
		VENUS_ASH = loose("venus_ash", MapColor.COLOR_YELLOW);
		SULFUR_ORE = ore("sulfur_ore", MapColor.COLOR_BROWN);

		PLUTO_ICE = rock("pluto_ice", MapColor.COLOR_LIGHT_BLUE, 1.2F);
		PLUTO_SNOW = loose("pluto_snow", MapColor.SNOW);
		FROST_ORE = ore("frost_ore", MapColor.COLOR_LIGHT_BLUE);

		ROCKET = put("rocket", RocketBlock::new, BlockBehaviour.Properties.of()
				.mapColor(MapColor.METAL)
				.strength(3.0F, 6.0F)
				.sound(SoundType.METAL)
				.requiresCorrectToolForDrops()
				.noOcclusion());
	}

	private static Block rock(String name, MapColor colour, float hardness) {
		return put(name, Block::new, BlockBehaviour.Properties.of()
				.mapColor(colour)
				.strength(hardness, 6.0F)
				.sound(SoundType.STONE)
				.requiresCorrectToolForDrops());
	}

	private static Block loose(String name, MapColor colour) {
		return put(name, Block::new, BlockBehaviour.Properties.of()
				.mapColor(colour)
				.strength(0.6F)
				.sound(SoundType.SAND));
	}

	private static Block ore(String name, MapColor colour) {
		return put(name, Block::new, BlockBehaviour.Properties.of()
				.mapColor(colour)
				.strength(3.0F, 3.0F)
				.sound(SoundType.STONE)
				.requiresCorrectToolForDrops());
	}

	private static Block put(String name, Function<BlockBehaviour.Properties, Block> factory,
	                         BlockBehaviour.Properties properties) {
		ResourceLocation key = PlanetsMod.id(name);
		//? if 1.21.1 {
		Block block = factory.apply(properties);
		//? } else {
		/*Block block = factory.apply(properties.setId(ResourceKey.create(Registries.BLOCK, key)));
		*///? }
		Registry.register(BuiltInRegistries.BLOCK, key, block);
		ALL.add(block);
		return block;
	}
}
