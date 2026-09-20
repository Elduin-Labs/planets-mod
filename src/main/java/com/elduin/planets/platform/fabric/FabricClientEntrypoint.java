package com.elduin.planets.platform.fabric;

//? fabric {

import com.elduin.planets.client.PlanetsClient;
import dev.kikugie.fletching_table.annotation.fabric.Entrypoint;
import net.fabricmc.api.ClientModInitializer;

@Entrypoint("client")
public class FabricClientEntrypoint implements ClientModInitializer {

	@Override
	public void onInitializeClient() {
		PlanetsClient.init();
	}

}
//?}
