package com.elduin.planets;

import com.elduin.planets.net.ModNetworking;
import com.elduin.planets.registry.ModBlocks;
import com.elduin.planets.registry.ModItems;
import com.elduin.planets.space.SpaceEffects;

import net.minecraft.resources.ResourceLocation;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class PlanetsMod {

	public static final String MOD_ID = /*$ mod_id*/ "planets";
	public static final String MOD_VERSION = /*$ mod_version*/ "1.0.0";
	public static final String MOD_FRIENDLY_NAME = /*$ mod_name*/ "Planets";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	public static void onInitialize() {
		ModBlocks.register();
		ModItems.register();
		ModNetworking.registerServerSide();
		SpaceEffects.register();
		LOGGER.info("{} {} is ready for launch", MOD_FRIENDLY_NAME, MOD_VERSION);
	}

	public static ResourceLocation id(String path) {
		return ResourceLocation.fromNamespaceAndPath(MOD_ID, path);
	}
}
