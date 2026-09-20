package com.elduin.planets.registry;

import java.util.ArrayList;
import java.util.List;

import com.elduin.planets.PlanetsMod;

import net.fabricmc.fabric.api.itemgroup.v1.FabricItemGroup;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;

public final class ModItems {

	public static final List<Item> ALL = new ArrayList<>();

	public static Item MOONSTONE;
	public static Item MARS_CRYSTAL;
	public static Item SULFUR;
	public static Item FROST_SHARD;
	public static Item OXYGEN_TANK;

	private ModItems() {
	}

	public static void register() {
		// One block item per block, in the same order the blocks were registered.
		for (Block block : ModBlocks.ALL) {
			blockItem(block);
		}

		MOONSTONE = simple("moonstone");
		MARS_CRYSTAL = simple("mars_crystal");
		SULFUR = simple("sulfur");
		FROST_SHARD = simple("frost_shard");
		OXYGEN_TANK = simple("oxygen_tank");

		CreativeModeTab tab = FabricItemGroup.builder()
				.title(Component.translatable("itemGroup.planets"))
				.icon(() -> new ItemStack(ModBlocks.ROCKET))
				.displayItems((parameters, output) -> {
					for (Item item : ALL) {
						output.accept(item);
					}
				})
				.build();
		Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, PlanetsMod.id("planets"), tab);
	}

	private static void blockItem(Block block) {
		ResourceLocation key = BuiltInRegistries.BLOCK.getKey(block);
		//? if 1.21.1 {
		BlockItem item = new BlockItem(block, new Item.Properties());
		//? } else {
		/*BlockItem item = new BlockItem(block, new Item.Properties()
				.useBlockDescriptionPrefix()
				.setId(ResourceKey.create(Registries.ITEM, key)));
		*///? }
		Registry.register(BuiltInRegistries.ITEM, key, item);
		ALL.add(item);
	}

	private static Item simple(String name) {
		ResourceLocation key = PlanetsMod.id(name);
		//? if 1.21.1 {
		Item item = new Item(new Item.Properties());
		//? } else {
		/*Item item = new Item(new Item.Properties().setId(ResourceKey.create(Registries.ITEM, key)));
		*///? }
		Registry.register(BuiltInRegistries.ITEM, key, item);
		ALL.add(item);
		return item;
	}
}
