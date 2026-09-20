package com.elduin.planets.platform.fabric;

//? fabric {

import com.elduin.planets.PlanetsMod;
import dev.kikugie.fletching_table.annotation.fabric.Entrypoint;
import net.fabricmc.api.ModInitializer;

@Entrypoint("main")
public class FabricEntrypoint implements ModInitializer {

	@Override
	public void onInitialize() {
		PlanetsMod.onInitialize();
	}
}
//?}
